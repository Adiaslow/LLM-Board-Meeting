"""
Base adapter interface for LLM providers.

This module defines the base interface that all LLM provider adapters must implement.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseLLMAdapter(ABC):
    """Base class for LLM provider adapters."""

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate a response from the LLM.

        Args:
            prompt: The user prompt to send to the LLM
            system_prompt: Optional system prompt for context
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            Dict containing the response and metadata
        """
        pass

    @abstractmethod
    async def get_token_count(self, text: str) -> int:
        """Get the number of tokens in the text.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens in the text
        """
        pass
