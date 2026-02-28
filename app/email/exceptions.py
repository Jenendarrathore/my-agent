class EmailProviderError(Exception):
    """Base exception for all email provider errors."""
    def __init__(self, message: str, provider: str = None):
        self.message = message
        self.provider = provider
        super().__init__(self.message)


class EmailAuthError(EmailProviderError):
    """Raised when authentication with the email provider fails."""
    pass


class EmailFetchError(EmailProviderError):
    """Raised when fetching messages or bodies from the provider fails."""
    pass


class EmailRateLimitError(EmailProviderError):
    """Raised when the provider rate limits requests."""
    pass
