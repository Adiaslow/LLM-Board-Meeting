# llm_board_meeting/consensus_management/models/entry.py

"""
Consensus Entry model for the LLM Board Meeting system.

This module defines the data structure representing a single consensus building process,
tracking the evolution of discussion, votes, and feedback from board members.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class ConsensusEntry:
    """Represents a single consensus building process.

    Attributes:
        topic: The topic under discussion.
        content: The content to build consensus on.
        source_role: Role that initiated the consensus process.
        consensus_type: Type of consensus mechanism to use.
        metadata: Additional metadata about the consensus process.
        status: Current status of the consensus process.
        created_at: When the consensus process was created.
        updated_at: When the consensus process was last updated.
        feedback_history: History of feedback from board members.
        supporting_votes: Votes in favor, mapped by role.
        opposing_votes: Votes against, mapped by role.
        iteration_count: Number of discussion iterations.
    """

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
