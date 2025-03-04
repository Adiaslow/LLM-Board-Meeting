"""
Ollama adapter implementation for local LLM inference.

This module provides integration with Ollama for running local LLM models.
"""

import json
from typing import Dict, Any, Optional
import aiohttp
from aiohttp import ClientTimeout

from .base import BaseLLMAdapter


class OllamaAdapter(BaseLLMAdapter):
    """Adapter for Ollama LLM integration."""

    def __init__(
        self,
        model_name: str = "tinyllama",
        base_url: str = "http://localhost:11434",
        timeout: int = 30,
        **kwargs: Any,
    ) -> None:
        """Initialize Ollama adapter.

        Args:
            model_name: Name of the Ollama model to use
            base_url: Base URL for Ollama API
            timeout: Request timeout in seconds
            **kwargs: Additional configuration options for Ollama
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip("/")
        self.timeout = ClientTimeout(total=timeout)
        self.options = kwargs

    async def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate a response using Ollama.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Ollama-specific parameters

        Returns:
            Dict containing the response and metadata
        """
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "system": system_prompt if system_prompt else "",
                "temperature": temperature,
                "options": {
                    **({"num_predict": max_tokens} if max_tokens else {}),
                    **self.options,  # Include initialization options
                    **kwargs,  # Allow overriding per-request
                },
            }

            try:
                async with session.post(
                    f"{self.base_url}/api/generate", json=payload, timeout=self.timeout
                ) as response:
                    response.raise_for_status()

                    # Handle NDJSON response format
                    response_text = await response.text()
                    # Take the last complete JSON object from the stream
                    json_responses = [
                        json.loads(line)
                        for line in response_text.strip().split("\n")
                        if line.strip()
                    ]
                    result = json_responses[-1] if json_responses else {}

                    return {
                        "content": result.get("response", ""),
                        "model": self.model_name,
                        "usage": {
                            "prompt_tokens": result.get("prompt_eval_count", 0),
                            "completion_tokens": result.get("eval_count", 0),
                            "total_tokens": (
                                result.get("prompt_eval_count", 0)
                                + result.get("eval_count", 0)
                            ),
                        },
                        "metadata": {"raw_response": result},
                    }

            except aiohttp.ClientError as e:
                raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")
            except Exception as e:
                raise RuntimeError(f"Error generating response: {str(e)}")

    async def get_token_count(self, text: str) -> int:
        """Get token count using Ollama's tokenizer.

        Args:
            text: Text to count tokens for

        Returns:
            Number of tokens in the text
        """
        async with aiohttp.ClientSession() as session:
            try:
                # Use generate endpoint with raw mode to get token count
                payload = {
                    "model": self.model_name,
                    "prompt": text,
                    "raw": True,
                    "options": {
                        "num_predict": 1
                    },  # Minimal prediction to just get token count
                }

                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=self.timeout,
                ) as response:
                    response.raise_for_status()
                    response_text = await response.text()
                    # Take the first JSON object which contains prompt evaluation info
                    json_responses = [
                        json.loads(line)
                        for line in response_text.strip().split("\n")
                        if line.strip()
                    ]
                    first_response = json_responses[0] if json_responses else {}

                    # Return the prompt evaluation count as token count
                    return first_response.get("prompt_eval_count", 0)

            except Exception as e:
                raise RuntimeError(f"Error counting tokens: {str(e)}")
