import logging
import random
import hashlib
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LLMResponse:
    content: Any
    model_name: str
    prompt_hash: str
    input_tokens: int
    output_tokens: int
    latency_ms: int

class MockLLMService:
    """
    Mock LLM Service for demonstrating email extraction.
    """

    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name

    async def extract_financial_data(self, email_text: str) -> LLMResponse:
        """
        Simulates an LLM call to extract financial data from email text.
        """
        logger.info(f"Mock LLM: Processing email with model {self.model_name}")
        
        # Simulate some logic based on text
        prompt_hash = hashlib.sha256(email_text.encode()).hexdigest()[:16]
        
        # Mock result
        content = {
            "amount": round(random.uniform(10.0, 500.0), 2),
            "currency": "USD",
            "merchant": "Mock Merchant",
            "category": "General",
            "is_transaction": True
        }
        
        if "uber" in email_text.lower():
            content["merchant"] = "Uber"
            content["category"] = "Transport"
        elif "amazon" in email_text.lower():
            content["merchant"] = "Amazon"
            content["category"] = "Shopping"

        return LLMResponse(
            content=content,
            model_name=self.model_name,
            prompt_hash=prompt_hash,
            input_tokens=random.randint(500, 1500),
            output_tokens=random.randint(200, 500),
            latency_ms=random.randint(800, 2500)
        )
