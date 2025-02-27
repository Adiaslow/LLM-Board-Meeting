# llm_board_meeting/health_monitoring/models/token_usage_record.py

"""
Token usage record model for the LLM Board Meeting system.

This module defines the data structure for tracking token usage in the system,
including prompt and completion tokens, and total tokens used.
"""

from typing import TypedDict


class TokenUsageRecord(TypedDict):
    """Type definition for token usage record.

    Attributes:
        timestamp: ISO format timestamp of the usage record.
        prompt_tokens: Number of prompt tokens used.
        completion_tokens: Number of completion tokens used.
        total_tokens: Total tokens used (prompt + completion).
    """

    timestamp: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
