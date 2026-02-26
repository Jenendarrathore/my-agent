
async def sample_task(ctx):
    """A sample base task."""
    print("Executing sample base task...")
    return "base_task_complete"

async def send_email(ctx, user_id: int):
    """Job to handle sending emails."""
    print(f"Sending email to user id: {user_id}")
    return "email_sent"
