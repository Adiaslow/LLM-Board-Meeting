# llm_board_meeting/health_monitoring/models/member_health.py

"""
Member health model for the LLM Board Meeting system.

This module defines the comprehensive health status data structure for board members,
integrating token usage, participation, and performance metrics.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict

from llm_board_meeting.health_monitoring.models.token_usage import TokenUsage
from llm_board_meeting.health_monitoring.models.participation import (
    ParticipationMetrics,
)
from llm_board_meeting.health_monitoring.models.performance import (
    PerformanceMetrics,
)


@dataclass
class MemberHealth:
    """Comprehensive health status for a board member.

    Attributes:
        member_id: Unique identifier for the member.
        role: Role of the board member.
        token_usage: Token usage metrics.
        participation: Participation metrics.
        performance: Performance metrics.
        last_health_check: Timestamp of last health check.
    """

    member_id: str
    role: str
    token_usage: TokenUsage = field(default_factory=TokenUsage)
    participation: ParticipationMetrics = field(default_factory=ParticipationMetrics)
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    last_health_check: datetime = field(default_factory=datetime.now)

    def calculate_health_score(self) -> float:
        """Calculate overall health score (0-1).

        Returns:
            Float between 0 and 1 indicating overall health.
        """
        # Token usage score (lower is better)
        token_efficiency = min(1.0, 1 - (self.token_usage.total_tokens / 1000000))

        # Participation score
        total_possible = max(1, self.participation.total_contributions)
        participation_rate = self.participation.total_contributions / total_possible

        # Performance score
        total_interactions = (
            self.performance.successful_interactions
            + self.performance.failed_interactions
        )
        success_rate = (
            self.performance.successful_interactions / total_interactions
            if total_interactions > 0
            else 0.0
        )

        # Weighted average of scores
        return token_efficiency * 0.3 + participation_rate * 0.3 + success_rate * 0.4

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary.

        Returns:
            Dict containing detailed health metrics.
        """
        return {
            "member_id": self.member_id,
            "role": self.role,
            "health_score": self.calculate_health_score(),
            "token_metrics": {
                "total_usage": self.token_usage.total_tokens,
                "usage_rate": self.token_usage.total_tokens
                / max(1, len(self.token_usage.usage_history)),
            },
            "participation_metrics": {
                "total_contributions": self.participation.total_contributions,
                "avg_response_time": sum(self.participation.response_times)
                / max(1, len(self.participation.response_times)),
                "contribution_distribution": self.participation.contribution_types,
            },
            "performance_metrics": {
                "success_rate": self.performance.successful_interactions
                / max(
                    1,
                    (
                        self.performance.successful_interactions
                        + self.performance.failed_interactions
                    ),
                ),
                "average_confidence": self.performance.average_confidence,
                "error_distribution": self.performance.error_counts,
            },
            "last_updated": self.last_health_check.isoformat(),
        }
