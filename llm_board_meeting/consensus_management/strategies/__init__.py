# llm_board_meeting/consensus_management/strategies/__init__.py

"""
Consensus building strategies for the LLM Board Meeting system.

This module provides different strategies for building consensus among board members,
including voting-based, discussion-based, hybrid, and facilitated approaches.
"""

from llm_board_meeting.consensus_management.strategies.base import ConsensusStrategy
from llm_board_meeting.consensus_management.strategies.voting import VotingBasedStrategy
from llm_board_meeting.consensus_management.strategies.discussion import (
    DiscussionBasedStrategy,
)
from llm_board_meeting.consensus_management.strategies.hybrid import HybridStrategy
from llm_board_meeting.consensus_management.strategies.facilitated import (
    FacilitatedStrategy,
)

__all__ = [
    "ConsensusStrategy",
    "VotingBasedStrategy",
    "DiscussionBasedStrategy",
    "HybridStrategy",
    "FacilitatedStrategy",
]
