from typing import Dict, Type, Optional
from app.email.providers.base import EmailProvider
from app.email.providers.gmail import GmailProvider

class ProviderFactory:
    _providers: Dict[str, Type[EmailProvider]] = {}

    @classmethod
    def register(cls, name: str, provider_cls: Type[EmailProvider]):
        cls._providers[name.lower()] = provider_cls

    @classmethod
    def get_provider(cls, name: str) -> EmailProvider:
        provider_cls = cls._providers.get(name.lower())
        if not provider_cls:
            raise ValueError(f"Unsupported provider: {name}")
        return provider_cls()

# Register initial providers
ProviderFactory.register("gmail", GmailProvider)
