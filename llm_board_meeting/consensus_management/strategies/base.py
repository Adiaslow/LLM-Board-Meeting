# llm_board_meeting/consensus_management/strategies/base.py

"""
Base consensus strategy for the LLM Board Meeting system.

This module provides the abstract base class for all consensus building strategies.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence

from llm_board_meeting.consensus_management.models import (
    ConsensusEntry,
    ConsensusConfig,
)
from llm_board_meeting.core.board_member import BoardMember


class ConsensusStrategy(ABC):
    """Abstract base class for consensus building strategies."""

    def __init__(self, config: ConsensusConfig) -> None:
        """Initialize strategy with configuration.

        Args:
            config: Configuration for consensus management.
        """
        self.config = config

    @abstractmethod
    async def process(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, Any]:
        """Process a consensus entry using this strategy.

        Args:
            entry: The consensus entry to process.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing process results.
        """
        pass
