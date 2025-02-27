# llm_board_meeting/core/board_member.py

"""
Base class for board members in the LLM Board Meeting system.

This module defines the core interface that all board members must implement,
following the Interface Segregation Principle from SOLID.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Sequence

from llm_board_meeting.consensus_management.models import ConsensusEntry


class BoardMember(ABC):
    """Abstract base class defining the interface for board members.

    Each board member represents an LLM with a specific role and personality
    profile in the board meeting system.

    Attributes:
        name: The name of the board member.
        role: The role of the board member (e.g., "Chairperson", "Technical Expert").
        expertise_areas: List of areas where this member has special knowledge.
        personality_profile: Configuration dict defining behavior characteristics.
    """

    def __init__(
        self,
        name: str,
        role: str,
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        role_specific_context: Dict[str, Any],
        llm_config: Dict[str, Any],
    ) -> None:
        """Initialize a new board member.

        Args:
            name: The name of the board member.
            role: The role of the board member.
            expertise_areas: List of expertise areas.
            personality_profile: Dict containing personality configuration.
            role_specific_context: Dict containing role-specific context.
            llm_config: Configuration for the LLM (temperature, etc.).
        """
        self.name = name
        self.role = role
        self.expertise_areas = expertise_areas
        self.personality_profile = personality_profile
        self.role_specific_context = role_specific_context
        self.llm_config = llm_config
        self._confidence_score = 0.0

    @abstractmethod
    async def generate_response(
        self, context: Dict[str, Any], prompt: str, **kwargs
    ) -> Dict[str, Any]:
        """Generate a response based on the given context and prompt.

        Args:
            context: The current context including meeting state and history.
            prompt: The specific prompt for this interaction.
            **kwargs: Additional keyword arguments for response generation.

        Returns:
            Dict containing the response and metadata.
        """
        pass

    @abstractmethod
    async def evaluate_proposal(
        self, proposal: Dict[str, Any], criteria: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate a proposal based on given criteria.

        Args:
            proposal: The proposal to evaluate.
            criteria: The criteria to evaluate against.

        Returns:
            Dict mapping criteria to scores.
        """
        pass

    @abstractmethod
    async def provide_feedback(
        self, target_content: Dict[str, Any], feedback_type: str
    ) -> Dict[str, Any]:
        """Provide feedback on specific content.

        Args:
            target_content: The content to provide feedback on.
            feedback_type: The type of feedback requested.

        Returns:
            Dict containing structured feedback.
        """
        pass

    @abstractmethod
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming message.

        Args:
            message: The message to process.

        Returns:
            Dict containing the response.
        """
        pass

    @abstractmethod
    async def contribute_to_discussion(
        self, topic: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Contribute to an ongoing discussion.

        Args:
            topic: The topic of discussion.
            context: Context information for the discussion.

        Returns:
            Dict containing the contribution.
        """
        pass

    @abstractmethod
    async def analyze_discussion(
        self, discussion_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze a discussion history.

        Args:
            discussion_history: List of discussion entries.

        Returns:
            Dict containing analysis results.
        """
        pass

    @abstractmethod
    async def summarize_content(
        self, content: Dict[str, Any], summary_type: str
    ) -> Dict[str, Any]:
        """Summarize content.

        Args:
            content: The content to summarize.
            summary_type: Type of summary requested.

        Returns:
            Dict containing the summary.
        """
        pass

    @abstractmethod
    async def validate_proposal(
        self, proposal: Dict[str, Any], criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate a proposal against criteria.

        Args:
            proposal: The proposal to validate.
            criteria: Validation criteria.

        Returns:
            Dict containing validation results.
        """
        pass

    @property
    def confidence_score(self) -> float:
        """Get the current confidence score of the board member.

        Returns:
            Float between 0 and 1 representing confidence.
        """
        return self._confidence_score

    @confidence_score.setter
    def confidence_score(self, value: float) -> None:
        """Set the confidence score of the board member.

        Args:
            value: Float between 0 and 1.

        Raises:
            ValueError: If value is not between 0 and 1.
        """
        if not 0 <= value <= 1:
            raise ValueError("Confidence score must be between 0 and 1")
        self._confidence_score = value
