# llm_board_meeting/health_monitoring/models/token_usage.py

"""
Token usage tracking model for the LLM Board Meeting system.

This module defines the data structures used to track and analyze token usage
by board members, including historical usage patterns and limits.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from llm_board_meeting.health_monitoring.models.token_usage_record import (
    TokenUsageRecord,
)


@dataclass
class TokenUsage:
    """Tracks token usage for a board member.

    Attributes:
        total_tokens: Total tokens used since last reset.
        prompt_tokens: Total prompt tokens used since last reset.
        completion_tokens: Total completion tokens used since last reset.
        last_reset: When the usage counters were last reset.
        usage_history: List of historical usage records.
    """

    total_tokens: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    last_reset: datetime = field(default_factory=datetime.now)
    usage_history: List[TokenUsageRecord] = field(default_factory=list)

    def add_usage(self, prompt_tokens: int, completion_tokens: int) -> None:
        """Add new token usage data.

        Args:
            prompt_tokens: Number of prompt tokens used.
            completion_tokens: Number of completion tokens used.
        """
        self.prompt_tokens += prompt_tokens
        self.completion_tokens += completion_tokens
        self.total_tokens = self.prompt_tokens + self.completion_tokens

        self.usage_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            }
        )
