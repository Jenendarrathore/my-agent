
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
