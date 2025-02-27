# llm_board_meeting/health_monitoring/models/performance.py

"""
Performance metrics model for the LLM Board Meeting system.

This module defines the data structures used to track and analyze performance
metrics of board members, including success rates and error patterns.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class PerformanceMetrics:
    """Tracks performance metrics for a board member.

    Attributes:
        successful_interactions: Number of successful interactions.
        failed_interactions: Number of failed interactions.
        average_confidence: Running average of confidence scores.
        error_counts: Distribution of error types encountered.
    """

    successful_interactions: int = 0
    failed_interactions: int = 0
    average_confidence: float = 0.0
    error_counts: Dict[str, int] = field(default_factory=dict)

    def record_interaction(
        self, success: bool, confidence: float, error_type: Optional[str] = None
    ) -> None:
        """Record a new interaction.

        Args:
            success: Whether the interaction was successful.
            confidence: Confidence level of the interaction.
            error_type: Type of error if the interaction failed.
        """
        if success:
            self.successful_interactions += 1
        else:
            self.failed_interactions += 1
            if error_type:
                self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        total_interactions = self.successful_interactions + self.failed_interactions
        self.average_confidence = (
            self.average_confidence * (total_interactions - 1) + confidence
        ) / total_interactions
