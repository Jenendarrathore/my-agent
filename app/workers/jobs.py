from app.core.database import AsyncSessionLocal
from app.jobs import JobRunner, EmailFetchJob, EmailExtractionJob

async def run_email_fetch(ctx, user_id: int, provider: str = "gmail", limit: int = 20, account_id: int = None):
    """ARQ Task: Fetch emails for a user."""
    async with AsyncSessionLocal() as db:
        runner = JobRunner(db)
        payload = {"user_id": user_id, "provider": provider, "limit": limit, "account_id": account_id}
        await runner.run_job(EmailFetchJob, "EMAIL_FETCH", payload, triggered_by="system")

async def run_email_extraction(ctx, batch_size: int = 10):
    """ARQ Task: Extract data from pending emails."""
    async with AsyncSessionLocal() as db:
        runner = JobRunner(db)
        payload = {"batch_size": batch_size}
        await runner.run_job(EmailExtractionJob, "EMAIL_EXTRACTION", payload, triggered_by="system")

async def sample_task(ctx):
    """A sample base task."""
    print("Executing sample base task...")
    return "base_task_complete"

async def send_email(ctx, user_id: int):
    """Job to handle sending emails."""
    print(f"Sending email to user id: {user_id}")
    return "email_sent"

async def send_otp_email(ctx, email: str, otp: str):
    """Job to handle sending OTP emails."""
    print(f"--- OTP EMAIL ---")
    print(f"To: {email}")
    print(f"OTP: {otp}")
    print(f"Valid for 5 minutes.")
    print(f"------------------")
    return "otp_email_sent"
