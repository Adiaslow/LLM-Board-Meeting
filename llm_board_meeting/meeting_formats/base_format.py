# llm_board_meeting/meeting_formats/base_format.py

"""
Base interface for meeting formats in the LLM Board Meeting system.

This module defines the core interface that all meeting formats must implement,
providing structure for different types of discussions and decision-making processes.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime

from llm_board_meeting.core.board_member import BoardMember


class MeetingFormat(ABC):
    """Abstract base class for meeting formats.

    Each format defines a specific structure for discussions, with distinct phases
    and objectives. Formats guide the flow of the meeting and determine how
    different board members interact.
    """

    def __init__(
        self,
        format_config: Dict[str, Any],
        time_allocation: Optional[Dict[str, int]] = None,
    ) -> None:
        """Initialize the meeting format.

        Args:
            format_config: Configuration for the meeting format.
            time_allocation: Optional dict mapping phases to time in minutes.
        """
        self.config = format_config
        self.time_allocation = time_allocation or self._get_default_time_allocation()
        self.current_phase = None
        self.phase_history = []
        self.start_time = None

    @abstractmethod
    def _get_default_time_allocation(self) -> Dict[str, int]:
        """Get the default time allocation for this format's phases.

        Returns:
            Dict mapping phase names to time in minutes.
        """
        pass

    @abstractmethod
    def get_phases(self) -> List[str]:
        """Get the list of phases for this format.

        Returns:
            List of phase names in order.
        """
        pass

    @abstractmethod
    def get_phase_prompt(self, phase: str, context: Dict[str, Any]) -> str:
        """Get the prompt template for a specific phase.

        Args:
            phase: The phase to get the prompt for.
            context: Current meeting context.

        Returns:
            Prompt template string for the phase.

        Raises:
            ValueError: If phase is not valid for this format.
        """
        pass

    @abstractmethod
    def get_phase_roles(self, phase: str) -> List[str]:
        """Get the roles that should participate in a phase.

        Args:
            phase: The phase to get roles for.

        Returns:
            List of role names that should participate.

        Raises:
            ValueError: If phase is not valid for this format.
        """
        pass

    @abstractmethod
    def check_phase_completion(self, phase: str, context: Dict[str, Any]) -> bool:
        """Check if a phase is complete based on context.

        Args:
            phase: The phase to check.
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.

        Raises:
            ValueError: If phase is not valid for this format.
        """
        pass

    def start_meeting(self) -> None:
        """Start the meeting, initializing timing and phase tracking."""
        self.start_time = datetime.now()
        self.current_phase = self.get_phases()[0]
        self.phase_history = [(self.current_phase, self.start_time)]

    def advance_phase(self, context: Dict[str, Any]) -> Optional[str]:
        """Advance to the next phase if current phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            Name of the new phase if advanced, None if no advance occurred.

        Raises:
            ValueError: If meeting hasn't started.
        """
        if not self.start_time:
            raise ValueError("Meeting hasn't started")

        if not self.check_phase_completion(self.current_phase, context):
            return None

        current_idx = self.get_phases().index(self.current_phase)
        if current_idx + 1 >= len(self.get_phases()):
            return None

        self.current_phase = self.get_phases()[current_idx + 1]
        self.phase_history.append((self.current_phase, datetime.now()))
        return self.current_phase

    def get_current_phase(self) -> Optional[str]:
        """Get the current phase name.

        Returns:
            Current phase name or None if meeting hasn't started.
        """
        return self.current_phase

    def get_time_remaining(self, phase: Optional[str] = None) -> int:
        """Get remaining time for a phase in minutes.

        Args:
            phase: Optional phase name, uses current phase if not specified.

        Returns:
            Remaining time in minutes.

        Raises:
            ValueError: If meeting hasn't started or phase is invalid.
        """
        if not self.start_time:
            raise ValueError("Meeting hasn't started")

        target_phase = phase or self.current_phase
        if target_phase not in self.time_allocation:
            raise ValueError(f"Invalid phase: {target_phase}")

        phase_start = None
        for p, t in reversed(self.phase_history):
            if p == target_phase:
                phase_start = t
                break

        if not phase_start:
            return self.time_allocation[target_phase]

        elapsed = (datetime.now() - phase_start).total_seconds() / 60
        return max(0, self.time_allocation[target_phase] - int(elapsed))

    def get_format_status(self) -> Dict[str, Any]:
        """Get the current status of the meeting format.

        Returns:
            Dict containing format status information.
        """
        return {
            "format_type": self.__class__.__name__,
            "current_phase": self.current_phase,
            "phase_history": [
                {"phase": p, "time": t.isoformat()} for p, t in self.phase_history
            ],
            "time_allocation": self.time_allocation,
            "start_time": self.start_time.isoformat() if self.start_time else None,
        }
