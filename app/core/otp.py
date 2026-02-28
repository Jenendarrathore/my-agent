import random
import string
from typing import Optional
from app.core.redis import redis_client

OTP_EXPIRY = 300  # 5 minutes in seconds

def generate_otp(length: int = 6) -> str:
    """Generate a random numeric OTP."""
    return "".join(random.choices(string.digits, k=length))
