"""
LLM provider management for the LLM Board Meeting system.

This module handles LLM provider configuration and initialization.
"""

from typing import Dict, Any, Optional, Type
from .adapters.base import BaseLLMAdapter
from .adapters.ollama import OllamaAdapter


class LLMProvider:
    """Manager class for LLM provider integration."""

    _adapters: Dict[str, Type[BaseLLMAdapter]] = {
        "ollama": OllamaAdapter,
    }

    def __init__(
        self, provider: str = "ollama", model_name: str = "llama2:7b", **kwargs: Any
    ) -> None:
        """Initialize LLM provider.

        Args:
            provider: Name of the LLM provider to use
            model_name: Name of the model to use
            **kwargs: Additional provider-specific configuration (excluding temperature)
        """
        if provider not in self._adapters:
            raise ValueError(f"Unsupported provider: {provider}")

        # Remove temperature from kwargs if present
        kwargs.pop("temperature", None)

        self.adapter = self._adapters[provider](model_name=model_name, **kwargs)

    async def generate_response(
        self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Any]:
        """Generate a response using the configured LLM provider.

        Args:
            prompt: The prompt to send to the LLM
            system_prompt: Optional system prompt
            **kwargs: Additional generation parameters

        Returns:
            Dict containing the response and metadata
        """
        return await self.adapter.generate_response(
            prompt=prompt, system_prompt=system_prompt, **kwargs
        )

    async def get_token_count(self, text: str) -> int:
        """Get token count for text.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens in the text
        """
        return await self.adapter.get_token_count(text)
