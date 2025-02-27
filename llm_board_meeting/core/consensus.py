# llm_board_meeting/core/consensus.py

"""
Base class for consensus mechanisms in the LLM Board Meeting system.

This module defines the core interface that all consensus mechanisms must implement,
following the Strategy Pattern and Dependency Inversion Principle from SOLID.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar, Generic

from llm_board_meeting.core.board_member import BoardMember

T = TypeVar("T")  # Type variable for the consensus input type
R = TypeVar("R")  # Type variable for the consensus result type


class ConsensusStrategy(Generic[T, R], ABC):
    """Abstract base class defining the interface for consensus mechanisms.

    Implements the Strategy Pattern to allow different consensus algorithms to be
    used interchangeably.
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the consensus mechanism.

        Args:
            config: Configuration parameters for the consensus mechanism.
        """
        self.config = config
        self._validate_config()

    @abstractmethod
    def _validate_config(self) -> None:
        """Validate the configuration parameters.

        Raises:
            ValueError: If configuration is invalid.
        """
        pass

    @abstractmethod
    async def build_consensus(
        self, board_members: List[BoardMember], input_data: T, context: Dict[str, Any]
    ) -> R:
        """Build consensus among board members.

        Args:
            board_members: List of board members participating in consensus.
            input_data: The data to build consensus on.
            context: Additional context for the consensus process.

        Returns:
            The consensus result.
        """
        pass

    @abstractmethod
    async def get_individual_positions(
        self, board_members: List[BoardMember], input_data: T, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get individual positions from each board member.

        Args:
            board_members: List of board members to get positions from.
            input_data: The data to evaluate.
            context: Additional context for position formation.

        Returns:
            Dict mapping board member names to their positions.
        """
        pass

    @abstractmethod
    async def analyze_disagreements(self, positions: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze disagreements between positions.

        Args:
            positions: Dict mapping board member names to their positions.

        Returns:
            Dict containing analysis of disagreements.
        """
        pass

    @abstractmethod
    async def resolve_conflicts(
        self,
        disagreements: Dict[str, Any],
        board_members: List[BoardMember],
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Attempt to resolve conflicts between positions.

        Args:
            disagreements: Dict containing analysis of disagreements.
            board_members: List of board members involved in conflicts.
            context: Additional context for conflict resolution.

        Returns:
            Dict containing resolution results.
        """
        pass

    @abstractmethod
    def get_confidence_score(self) -> float:
        """Get the confidence score for the consensus.

        Returns:
            Float between 0 and 1 indicating confidence in the consensus.
        """
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the consensus mechanism.

        Returns:
            Dict containing status information.
        """
        return {
            "type": self.__class__.__name__,
            "config": self.config,
            "confidence_score": self.get_confidence_score(),
        }
