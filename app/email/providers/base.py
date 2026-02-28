from abc import ABC, abstractmethod
from typing import List, Optional, Any
from app.email.dto import EmailMessage


class EmailProvider(ABC):
    """
    Abstract Base Class for email providers.
    Implementations must be stateless and accept credentials at runtime.
    """

    @abstractmethod
    async def connect(self, credentials: Any) -> None:
        """
        Establish a connection or validate credentials.
        :param credentials: Provider-specific credentials (e.g., access token).
        """
        pass

    @abstractmethod
    async def fetch_messages(
        self, 
        cursor: Optional[str] = None, 
        limit: int = 50
    ) -> List[EmailMessage]:
        """
        Fetch a list of normalized email messages.
        :param cursor: Optional pagination cursor.
        :param limit: Number of messages to fetch.
        :return: List of EmailMessage DTOs.
        """
        pass

    @abstractmethod
    async def fetch_message_body(self, message_id: str) -> Optional[EmailMessage]:
        """
        Fetch the full body (text/HTML) for a specific message.
        :param message_id: The provider-specific message ID.
        :return: EmailMessage DTO with body fields populated.
        """
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close connections and cleanup resources."""
        pass
