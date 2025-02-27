# llm_board_meeting/health_monitoring/monitor.py

"""
Health monitoring service for the LLM Board Meeting system.

This module provides functionality to track and analyze the health metrics of board members,
including token usage, participation patterns, and performance indicators.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from llm_board_meeting.core.board_member import BoardMember
from llm_board_meeting.health_monitoring.models import (
    MemberHealth,
    TokenUsage,
    ParticipationMetrics,
    PerformanceMetrics,
)


class HealthMonitor:
    """Service for monitoring and managing board member health."""

    def __init__(self, token_limit_per_hour: int = 100000):
        """Initialize the health monitor.

        Args:
            token_limit_per_hour: Maximum tokens allowed per hour per member.
        """
        self.member_health: Dict[str, MemberHealth] = {}
        self.token_limit_per_hour = token_limit_per_hour
        self._last_cleanup = datetime.now()

    def register_member(self, member_id: str, role: str) -> None:
        """Register a new board member for health tracking.

        Args:
            member_id: Unique identifier for the member.
            role: Role of the board member.
        """
        if member_id not in self.member_health:
            self.member_health[member_id] = MemberHealth(member_id=member_id, role=role)

    def record_token_usage(
        self, member_id: str, prompt_tokens: int, completion_tokens: int
    ) -> bool:
        """Record token usage for a member and check if within limits.

        Args:
            member_id: Member identifier.
            prompt_tokens: Number of prompt tokens used.
            completion_tokens: Number of completion tokens used.

        Returns:
            bool: True if usage is within limits, False otherwise.
        """
        if member_id not in self.member_health:
            return False

        member = self.member_health[member_id]
        member.token_usage.add_usage(prompt_tokens, completion_tokens)

        # Check hourly limit
        hour_ago = datetime.now() - timedelta(hours=1)
        recent_usage = sum(
            record["total_tokens"]
            for record in member.token_usage.usage_history
            if datetime.fromisoformat(record["timestamp"]) > hour_ago
        )

        return recent_usage <= self.token_limit_per_hour

    def record_contribution(
        self,
        member_id: str,
        contribution_type: str,
        response_time: float,
        success: bool,
        confidence: float,
        error_type: Optional[str] = None,
    ) -> None:
        """Record a member's contribution and its outcomes.

        Args:
            member_id: Member identifier.
            contribution_type: Type of contribution made.
            response_time: Time taken to respond (in seconds).
            success: Whether the contribution was successful.
            confidence: Confidence level of the contribution.
            error_type: Type of error if the contribution failed.
        """
        if member_id not in self.member_health:
            return

        member = self.member_health[member_id]
        member.participation.record_contribution(contribution_type, response_time)
        member.performance.record_interaction(success, confidence, error_type)
        member.last_health_check = datetime.now()

    def get_member_health(self, member_id: str) -> Optional[Dict]:
        """Get health summary for a specific member.

        Args:
            member_id: Member identifier.

        Returns:
            Optional[Dict]: Health summary if member exists, None otherwise.
        """
        if member_id not in self.member_health:
            return None
        return self.member_health[member_id].get_health_summary()

    def get_system_health(self) -> Dict:
        """Get overall system health summary.

        Returns:
            Dict: System-wide health metrics.
        """
        if not self.member_health:
            return {"status": "no_members", "timestamp": datetime.now().isoformat()}

        total_tokens = sum(
            member.token_usage.total_tokens for member in self.member_health.values()
        )
        avg_health = sum(
            member.calculate_health_score() for member in self.member_health.values()
        ) / len(self.member_health)

        return {
            "status": "healthy" if avg_health > 0.7 else "needs_attention",
            "timestamp": datetime.now().isoformat(),
            "member_count": len(self.member_health),
            "total_token_usage": total_tokens,
            "average_health_score": avg_health,
            "members_needing_attention": [
                member_id
                for member_id, member in self.member_health.items()
                if member.calculate_health_score() < 0.7
            ],
        }

    def cleanup_old_data(self, retention_days: int = 7) -> None:
        """Clean up old usage history data.

        Args:
            retention_days: Number of days to retain data.
        """
        cutoff = datetime.now() - timedelta(days=retention_days)

        for member in self.member_health.values():
            member.token_usage.usage_history = [
                record
                for record in member.token_usage.usage_history
                if datetime.fromisoformat(record["timestamp"]) > cutoff
            ]

            # Reset counters if all history is cleaned
            if not member.token_usage.usage_history:
                member.token_usage.total_tokens = 0
                member.token_usage.prompt_tokens = 0
                member.token_usage.completion_tokens = 0

    def get_health_alerts(self) -> List[Dict]:
        """Get list of health alerts for members needing attention.

        Returns:
            List[Dict]: List of health alerts.
        """
        alerts = []
        for member_id, member in self.member_health.items():
            health_score = member.calculate_health_score()
            if health_score < 0.7:
                alerts.append(
                    {
                        "member_id": member_id,
                        "role": member.role,
                        "health_score": health_score,
                        "timestamp": datetime.now().isoformat(),
                        "issues": self._identify_health_issues(member),
                    }
                )
        return alerts

    def _identify_health_issues(self, member: MemberHealth) -> List[str]:
        """Identify specific health issues for a member.

        Args:
            member: MemberHealth instance to analyze.

        Returns:
            List[str]: List of identified issues.
        """
        issues = []

        # Check token usage
        hour_ago = datetime.now() - timedelta(hours=1)
        recent_usage = sum(
            record["total_tokens"]
            for record in member.token_usage.usage_history
            if datetime.fromisoformat(record["timestamp"]) > hour_ago
        )
        if recent_usage > self.token_limit_per_hour * 0.9:
            issues.append("high_token_usage")

        # Check participation
        if not member.participation.last_contribution:
            issues.append("no_participation")
        elif datetime.now() - member.participation.last_contribution > timedelta(
            hours=1
        ):
            issues.append("low_participation")

        # Check performance
        if member.performance.average_confidence < 0.6:
            issues.append("low_confidence")

        total_interactions = (
            member.performance.successful_interactions
            + member.performance.failed_interactions
        )
        if total_interactions > 0:
            success_rate = (
                member.performance.successful_interactions / total_interactions
            )
            if success_rate < 0.8:
                issues.append("high_failure_rate")

        return issues

    async def update_member_metrics(
        self, member: "BoardMember", contribution: Dict[str, Any]
    ) -> None:
        """Update health metrics for a member based on their contribution.

        Args:
            member: The board member whose metrics to update.
            contribution: The contribution data from the member.
        """
        if member.name not in self.member_health:
            return

        member_health = self.member_health[member.name]

        # Update token usage if available
        if "token_usage" in contribution:
            usage = contribution["token_usage"]
            member_health.token_usage.add_usage(
                usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
            )

        # Update participation metrics
        member_health.participation.record_contribution(
            contribution_type=contribution.get("type", "discussion"),
            response_time=contribution.get("response_time", 0.0),
        )

        # Update performance metrics
        member_health.performance.record_interaction(
            success=contribution.get("success", True),
            confidence=contribution.get("confidence", 0.8),
            error_type=contribution.get("error_type"),
        )

    async def get_meeting_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics for the current meeting.

        Returns:
            Dict containing meeting-wide health metrics.
        """
        return {
            member_id: member.get_health_summary()
            for member_id, member in self.member_health.items()
        }
