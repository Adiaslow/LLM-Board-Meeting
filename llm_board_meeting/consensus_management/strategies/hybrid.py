# llm_board_meeting/consensus_management/strategies/hybrid.py

"""
Hybrid consensus strategy for the LLM Board Meeting system.

This module implements a hybrid approach combining voting and discussion.
"""

from typing import Any, Dict, Sequence

from llm_board_meeting.consensus_management.strategies.base import ConsensusStrategy
from llm_board_meeting.consensus_management.strategies.voting import VotingBasedStrategy
from llm_board_meeting.consensus_management.strategies.discussion import (
    DiscussionBasedStrategy,
)
from llm_board_meeting.consensus_management.models import ConsensusEntry
from llm_board_meeting.core.board_member import BoardMember


class HybridStrategy(ConsensusStrategy):
    """Implements hybrid consensus building combining voting and discussion."""

    def __init__(self, config) -> None:
        """Initialize HybridStrategy.

        Args:
            config: Configuration for consensus management.
        """
        super().__init__(config)
        self.voting_strategy = VotingBasedStrategy(config)
        self.discussion_strategy = DiscussionBasedStrategy(config)

    async def process(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, Any]:
        """Process consensus using hybrid approach.

        Args:
            entry: The consensus entry to process.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing hybrid process results and consensus status.
        """
        # Start with voting
        vote_result = await self.voting_strategy.process(entry, board_members)

        if vote_result["status"] == "achieved":
            return vote_result

        # If voting inconclusive, proceed with discussion
        discussion_result = await self.discussion_strategy.process(entry, board_members)

        return {
            "status": discussion_result["status"],
            "vote_result": vote_result,
            "discussion_result": discussion_result,
            "rounds": vote_result["rounds"] + discussion_result["rounds"],
        }
