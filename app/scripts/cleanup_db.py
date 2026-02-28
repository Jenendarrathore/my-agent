import asyncio
import logging
import argparse
from sqlalchemy import text, delete
from app.core.database import AsyncSessionLocal, engine, Base
from app.models import (
    User, Role, Category, Transaction, ConnectedAccount,
    Email, EmailExtraction, Job, LLMTransaction
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseCleaner:
    def __init__(self, session):
        self.session = session

    async def clean_llm_transactions(self):
        logger.info("Cleaning LLM Transactions...")
        await self.session.execute(delete(LLMTransaction))

    async def clean_email_extractions(self):
        logger.info("Cleaning Email Extractions...")
        await self.session.execute(delete(EmailExtraction))

    async def clean_transactions(self):
        logger.info("Cleaning Financial Transactions...")
        await self.session.execute(delete(Transaction))

    async def clean_emails(self):
        logger.info("Cleaning Emails...")
        await self.session.execute(delete(Email))

    async def clean_connected_accounts(self):
        logger.info("Cleaning Connected Accounts...")
        await self.session.execute(delete(ConnectedAccount))

    async def clean_categories(self):
        logger.info("Cleaning Categories...")
        await self.session.execute(delete(Category))

    async def clean_jobs(self):
        logger.info("Cleaning Jobs...")
        await self.session.execute(delete(Job))

    async def clean_users(self):
        logger.info("Cleaning Users...")
        # Users might have many dependencies, CASCADE TRUNCATE is safer but 
        # for explicit method we just delete.
        await self.session.execute(delete(User))

    async def clean_roles(self):
        logger.info("Cleaning Roles...")
        await self.session.execute(delete(Role))

    async def reset_sequences(self):
        """Reset all postgres sequences to restart IDs from 1."""
        logger.info("Resetting all ID sequences...")
        tables = Base.metadata.sorted_tables
        for table in tables:
            await self.session.execute(text(f'ALTER SEQUENCE IF EXISTS "{table.name}_id_seq" RESTART WITH 1;'))

async def run_cleanup(skip_models: list = None, force: bool = False):
    if skip_models is None:
        skip_models = [s.lower() for s in skip_models] if skip_models else []
    else:
        skip_models = [s.lower() for s in skip_models]

    if not force:
        print("\n⚠️  WARNING: Explicit cleanup initiated.")
        if skip_models:
            print(f"Skipping: {', '.join(skip_models)}")
        confirm = input("Proceed? (y/N): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            return

    async with AsyncSessionLocal() as session:
        cleaner = DatabaseCleaner(session)
        
        # Define execution order (Dependencies first - Bottom to Top)
        tasks = [
            ("llmtransaction", cleaner.clean_llm_transactions),
            ("emailextraction", cleaner.clean_email_extractions),
            ("transaction", cleaner.clean_transactions),
            ("email", cleaner.clean_emails),
            ("connectedaccount", cleaner.clean_connected_accounts),
            ("category", cleaner.clean_categories),
            ("job", cleaner.clean_jobs),
            ("user", cleaner.clean_users),
            ("role", cleaner.clean_roles),
        ]

        try:
            executed_any = False
            for name, method in tasks:
                # Check if skipped (handle plural/singular)
                if name not in skip_models and f"{name}s" not in skip_models:
                    await method()
                    executed_any = True
            
            if executed_any:
                await cleaner.reset_sequences()
                await session.commit()
                logger.info("✨ Database cleaned successfully!")
            else:
                logger.info("ℹ️ No cleanup methods were executed based on your skip list.")

        except Exception as e:
            await session.rollback()
            logger.error(f"❌ Cleanup failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
        finally:
            await session.close()
            await engine.dispose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip", nargs="+", help="Explicitly skip specific models")
    parser.add_argument("-f", "--force", action="store_true")
    args = parser.parse_args()
    asyncio.run(run_cleanup(skip_models=args.skip, force=args.force))
