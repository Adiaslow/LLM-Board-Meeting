# llm_board_meeting/consensus_management/models.py

"""
Data models for consensus management in the LLM Board Meeting system.

This module defines the data structures used for managing consensus building,
including entries and configuration.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class ConsensusConfig:
    """Configuration for consensus management."""

    voting_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "Chairperson": 1.2,
            "Secretary": 1.0,
            "DevilsAdvocate": 1.1,
            "Synthesizer": 1.0,
            "TechnicalExpert": 1.1,
            "StrategicThinker": 1.1,
            "FinancialAnalyst": 1.1,
            "UserAdvocate": 1.0,
            "Innovator": 0.9,
            "Pragmatist": 1.0,
            "EthicalOverseer": 1.1,
            "Facilitator": 1.0,
            "Futurist": 0.9,
        }
    )
    max_discussion_rounds: int = 5
    discussion_agreement_threshold: float = 0.75
    min_participants: int = 3
    timeout_minutes: int = 30


@dataclass
class ConsensusEntry:
    """Represents a single consensus building process."""

    topic: str
    content: Dict[str, Any]
    source_role: str
    consensus_type: str = "auto"
    metadata: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    feedback_history: List[Dict[str, Any]] = field(default_factory=list)
    supporting_votes: Dict[str, float] = field(default_factory=dict)
    opposing_votes: Dict[str, float] = field(default_factory=dict)
    iteration_count: int = 0

    def update_status(self, new_status: str) -> None:
        """Update entry status and timestamp.

        Args:
            new_status: New status to set.
        """
        self.status = new_status
        self.updated_at = datetime.now()

    def add_feedback(self, feedback: Dict[str, Any]) -> None:
        """Add feedback to history.

        Args:
            feedback: Feedback to add.
        """
        self.feedback_history.append(
            {
                "timestamp": datetime.now(),
                "content": feedback,
            }
        )
        self.updated_at = datetime.now()

    def record_vote(self, role: str, vote: float, is_supporting: bool) -> None:
        """Record a vote from a board member.

        Args:
            role: Role of the voting member.
            vote: Vote value between 0 and 1.
            is_supporting: Whether this is a supporting vote.
        """
        if is_supporting:
            self.supporting_votes[role] = vote
        else:
            self.opposing_votes[role] = vote
        self.updated_at = datetime.now()

    def increment_iteration(self) -> None:
        """Increment the iteration count."""
        self.iteration_count += 1
        self.updated_at = datetime.now()
