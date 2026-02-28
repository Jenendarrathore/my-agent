import asyncio
from typing import List, Optional, Any
from datetime import datetime, timezone
from app.email.dto import EmailMessage
from app.email.providers.base import EmailProvider
from app.email.exceptions import EmailAuthError

class MockEmailProvider(EmailProvider):
    async def connect(self, credentials: Any) -> None:
        if credentials != "valid-token":
            raise EmailAuthError("Invalid mock token", provider="mock")
        print("Mock: Connected")

    async def fetch_messages(self, cursor: Optional[str] = None, limit: int = 50) -> List[EmailMessage]:
        return [
            EmailMessage(
                provider="mock",
                provider_message_id="mock-1",
                from_email="sender@example.com",
                to_emails=["receiver@example.com"],
                subject="Test Subject",
                received_at=datetime.now(timezone.utc)
            )
        ]

    async def fetch_message_body(self, message_id: str) -> Optional[EmailMessage]:
        return EmailMessage(
            provider="mock",
            provider_message_id=message_id,
            from_email="sender@example.com",
            to_emails=["receiver@example.com"],
            subject="Test Subject",
            body_text="Hello World",
            received_at=datetime.now(timezone.utc)
        )

    async def disconnect(self) -> None:
        print("Mock: Disconnected")

async def test_mock_provider():
    provider = MockEmailProvider()
    try:
        await provider.connect("valid-token")
        messages = await provider.fetch_messages()
        print(f"Fetched {len(messages)} messages")
        print(f"First message subject: {messages[0].subject}")
        
        body_msg = await provider.fetch_message_body("mock-1")
        print(f"Body: {body_msg.body_text}")
        
        await provider.disconnect()
        print("Mock verification PASSED")
    except Exception as e:
        print(f"Mock verification FAILED: {e}")

if __name__ == "__main__":
    asyncio.run(test_mock_provider())
