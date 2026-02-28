from typing import Any, Dict, Optional
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.jobs.base import BaseJob
from app.models.email import Email
from app.services.llm import MockLLMService
from app.services.email_extraction_service import EmailExtractionService
from app.services.llm_transaction_service import LLMTransactionService
from app.services.transaction_service import TransactionService
from app.services.category_service import CategoryService
from app.schemas.email_extraction import EmailExtractionCreate
from app.schemas.llm_transaction import LLMTransactionCreate
from app.schemas.transaction import TransactionCreate
import logging

logger = logging.getLogger(__name__)

class EmailExtractionJob(BaseJob):
    """
    Job to process PENDING emails using LLM and create financial transactions.
    """

    async def run(self) -> Dict[str, Any]:
        batch_size = self.input_payload.get("batch_size", 10)
        reprocess = self.input_payload.get("reprocess", False)
        
        # 1. Fetch emails to process
        query = select(Email)
        if not reprocess:
            query = query.where(Email.extraction_status == "PENDING")
        
        query = query.limit(batch_size)
        result = await self.db.execute(query)
        emails = result.scalars().all()
        
        logger.info(f"Processing batch of {len(emails)} emails")

        llm = MockLLMService()
        ext_service = EmailExtractionService(self.db)
        llm_tx_service = LLMTransactionService(self.db)
        tx_service = TransactionService(self.db)
        cat_service = CategoryService(self.db)

        processed_count = 0
        transaction_count = 0

        for email in emails:
            try:
                # 2. Extract Data via LLM
                # (In a real app, we'd fetch the full body here if needed)
                email_text = f"Subject: {email.subject}"
                llm_res = await llm.extract_financial_data(email_text)

                # 3. Record LLM Transaction
                llm_tx_in = LLMTransactionCreate(
                    job_id=self.job_record.id,
                    model_name=llm_res.model_name,
                    provider="openai", # Mock
                    prompt_hash=llm_res.prompt_hash,
                    input_tokens=llm_res.input_tokens,
                    output_tokens=llm_res.output_tokens,
                    total_tokens=llm_res.input_tokens + llm_res.output_tokens,
                    latency_ms=llm_res.latency_ms
                )
                await llm_tx_service.create_transaction(llm_tx_in)

                # 4. Save Extraction result
                ext_in = EmailExtractionCreate(
                    email_id=email.id,
                    status="SUCCESS" if llm_res.content.get("is_transaction") else "SKIPPED",
                    extracted_json=llm_res.content,
                    model_used=llm_res.model_name,
                    prompt_hash=llm_res.prompt_hash
                )
                await ext_service.create_extraction(ext_in)

                # 5. Create Financial Transaction if applicable
                if llm_res.content.get("is_transaction"):
                    # Find or create category
                    cat_name = llm_res.content.get("category", "General")
                    cat = await cat_service.get_category_by_name(email.user_id, cat_name)
                    if not cat:
                        # Simple mock: just use a default or create it
                        from app.schemas.category import CategoryCreate
                        cat = await cat_service.create_category(CategoryCreate(
                            name=cat_name,
                            type="expense"
                        ), email.user_id)

                    tx_in = TransactionCreate(
                        user_id=email.user_id,
                        amount=llm_res.content.get("amount"),
                        type="expense",
                        occurred_at=email.received_at, # Use email date as default
                        category_id=cat.id,
                        notes=f"Auto-extracted from email: {email.subject}"
                    )
                    await tx_service.create_transaction(tx_in, email.user_id)
                    transaction_count += 1

                # 6. Update Email Status
                email.extraction_status = "COMPLETED"
                processed_count += 1
                
                await self.db.commit()

            except Exception as e:
                logger.error(f"Failed to process email {email.id}: {str(e)}")
                email.extraction_status = "FAILED"
                await self.db.commit()

        return {
            "processed_count": processed_count,
            "transaction_count": transaction_count
        }
