# llm_board_meeting/consensus_management/strategies/voting.py

"""
Voting-based consensus strategy for the LLM Board Meeting system.

This module implements a weighted voting approach to consensus building.
"""

from typing import Any, Dict, Sequence

from llm_board_meeting.consensus_management.strategies.base import ConsensusStrategy
from llm_board_meeting.consensus_management.models import ConsensusEntry
from llm_board_meeting.core.board_member import BoardMember


class VotingBasedStrategy(ConsensusStrategy):
    """Implements voting-based consensus building."""

    async def process(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, Any]:
        """Process consensus through weighted voting.

        Args:
            entry: The consensus entry to process.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing voting results and consensus status.
        """
        votes = await self._collect_votes(entry, board_members)
        weighted_score = self._calculate_weighted_score(votes)

        return {
            "status": "achieved" if weighted_score >= 0.75 else "in_progress",
            "weighted_score": weighted_score,
            "votes": votes,
            "rounds": 1,
        }

    async def _collect_votes(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, float]:
        """Collect votes from board members.

        Args:
            entry: The consensus entry to vote on.
            board_members: Sequence of board members participating in voting.

        Returns:
            Dict mapping member roles to their votes.
        """
        votes = {}
        for member in board_members:
            vote = await member.evaluate_proposal(
                entry.content, entry.metadata.get("criteria", {})
            )
            votes[member.role] = vote * self.config.voting_weights.get(member.role, 1.0)
        return votes

    def _calculate_weighted_score(self, votes: Dict[str, float]) -> float:
        """Calculate weighted consensus score from votes.

        Args:
            votes: Dict mapping member roles to their votes.

        Returns:
            Weighted consensus score between 0 and 1.
        """
        if not votes:
            return 0.0

        total_weight = sum(self.config.voting_weights.get(role, 1.0) for role in votes)
        weighted_sum = sum(votes.values())

        return weighted_sum / total_weight if total_weight > 0 else 0.0
