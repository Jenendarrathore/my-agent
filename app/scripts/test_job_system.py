import asyncio
import logging
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.jobs import JobRunner, EmailFetchJob, EmailExtractionJob
from app.services.user_service import UserService
from app.services.connected_account_service import ConnectedAccountService
from app.schemas.user import UserCreate
from unittest.mock import patch, MagicMock
from app.email.dto import EmailMessage

# --- Mock Provider for Testing ---
class MockGmailProvider:
    def __init__(self):
        self.connected = False
    async def connect(self, creds): self.connected = True
    async def fetch_messages(self, cursor=None, limit=50):
        from datetime import datetime, timezone
        ts = int(datetime.now().timestamp())
        return [
            EmailMessage(
                provider="gmail",
                provider_message_id=f"msg-{ts}-{i}",
                from_email="billing@uber.com",
                to_emails=["user@example.com"],
                subject=f"Your Uber Trip {i}",
                received_at=datetime.now(timezone.utc)
            ) for i in range(3)
        ]
    async def disconnect(self): self.connected = False
# ---------------------------------

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_jobs():
    async for db in get_db():
        try:
            # 1. Setup Test User and Account
            user_service = UserService(db)
            conn_service = ConnectedAccountService(db)
            
            ts = int(datetime.now().timestamp())
            user_in = UserCreate(
                name="Job Tester",
                username=f"job_tester_{ts}",
                primary_email=f"job_tester_{ts}@example.com",
                password="SecurePassword123!"
            )
            user = await user_service.create_user(user_in)
            logger.info(f"Created test user: {user.id}")

            from app.schemas.connected_account import ConnectedAccountCreate
            conn_in = ConnectedAccountCreate(
                user_id=user.id,
                provider="gmail",
                email=f"test_{ts}@gmail.com",
                access_token="valid-token", # Works with Mock Gmail Provider
                refresh_token="refresh-123",
                token_expiry=datetime.now(timezone.utc)
            )
            await conn_service.create_account(conn_in)
            await db.commit()

            runner = JobRunner(db)

            # 2. Run EmailFetchJob
            logger.info("--- Running EmailFetchJob ---")
            fetch_payload = {
                "user_id": user.id,
                "provider": "gmail",
                "limit": 5
            }
            
            with patch("app.jobs.email_fetch.GmailProvider", return_value=MockGmailProvider()):
                fetch_job_record = await runner.run_job(EmailFetchJob, "EMAIL_FETCH", fetch_payload)
            
            logger.info(f"Fetch Job Status: {fetch_job_record.status}")
            logger.info(f"Fetch Job Output: {fetch_job_record.output_payload}")

            # 3. Run EmailExtractionJob
            logger.info("--- Running EmailExtractionJob ---")
            extract_payload = {
                "batch_size": 10
            }
            extract_job_record = await runner.run_job(EmailExtractionJob, "EMAIL_EXTRACTION", extract_payload)
            logger.info(f"Extraction Job Status: {extract_job_record.status}")
            logger.info(f"Extraction Job Output: {extract_job_record.output_payload}")

            # 4. Final verification of side effects
            from app.services.email_service import EmailService
            from app.services.transaction_service import TransactionService
            from app.services.llm_transaction_service import LLMTransactionService
            
            email_service = EmailService(db)
            emails = await email_service.list_user_emails(user.id)
            logger.info(f"Verified Emails Count: {len(emails)}")

            tx_service = TransactionService(db)
            txs = await tx_service.list_user_transactions(user.id)
            logger.info(f"Verified Transactions Count: {len(txs)}")

            # Check LLM transactions
            from sqlalchemy import select
            from app.models.llm_transaction import LLMTransaction
            res = await db.execute(select(LLMTransaction).where(LLMTransaction.job_id == extract_job_record.id))
            llm_txs = res.scalars().all()
            logger.info(f"Verified LLM Transactions Count: {len(llm_txs)}")

            if fetch_job_record.status == "SUCCESS" and extract_job_record.status == "SUCCESS" and len(txs) > 0:
                logger.info("CORE JOB SYSTEM VERIFICATION: PASSED")
            else:
                logger.error("CORE JOB SYSTEM VERIFICATION: FAILED")

            break # Only need one iteration from get_db
        except Exception as e:
            logger.error(f"Verification FAILED: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            break

if __name__ == "__main__":
    asyncio.run(verify_jobs())
