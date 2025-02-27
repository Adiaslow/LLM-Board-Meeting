# llm_board_meeting/health_monitoring/models/participation.py

"""
Participation metrics model for the LLM Board Meeting system.

This module defines the data structures used to track and analyze participation
patterns of board members, including contribution frequency and response times.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class ParticipationMetrics:
    """Tracks participation metrics for a board member.

    Attributes:
        total_contributions: Total number of contributions made.
        contribution_types: Distribution of contribution types.
        last_contribution: Timestamp of the last contribution.
        response_times: List of response times in seconds.
        intervention_count: Number of interventions made.
    """

    total_contributions: int = 0
    contribution_types: Dict[str, int] = field(default_factory=dict)
    last_contribution: Optional[datetime] = None
    response_times: List[float] = field(default_factory=list)
    intervention_count: int = 0

    def record_contribution(self, contribution_type: str, response_time: float) -> None:
        """Record a new contribution.

        Args:
            contribution_type: Type of contribution made.
            response_time: Time taken to respond in seconds.
        """
        self.total_contributions += 1
        self.contribution_types[contribution_type] = (
            self.contribution_types.get(contribution_type, 0) + 1
        )
        self.last_contribution = datetime.now()
        self.response_times.append(response_time)
