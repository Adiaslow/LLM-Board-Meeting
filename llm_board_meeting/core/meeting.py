# llm_board_meeting/core/meeting.py

"""
Core Meeting implementation for the LLM Board Meeting system.

This module provides the main Meeting class that orchestrates board member interactions,
manages meeting state, and coordinates the overall meeting process.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
import asyncio

from ..context_management.manager import ContextManager
from ..consensus_management.manager import ConsensusManager
from ..health_monitoring.monitor import HealthMonitor
from .board_member import BoardMember


class MeetingState(Enum):
    """Enumeration of possible meeting states."""

    INITIALIZED = "initialized"
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    CONSENSUS_BUILDING = "consensus_building"
    WRAPPING_UP = "wrapping_up"
    CONCLUDED = "concluded"
    PAUSED = "paused"
    ERROR = "error"


class Meeting:
    """Main meeting orchestrator class.

    Responsible for:
    - Managing meeting lifecycle
    - Coordinating member interactions
    - Maintaining meeting state
    - Managing context and consensus
    - Monitoring member health
    """

    def __init__(
        self,
        meeting_id: str,
        format_config: Dict[str, Any],
        members: List[BoardMember],
        context_config: Optional[Dict[str, Any]] = None,
        consensus_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize a new meeting.

        Args:
            meeting_id: Unique identifier for the meeting
            format_config: Configuration for the meeting format
            members: List of board members participating
            context_config: Optional configuration for context management
            consensus_config: Optional configuration for consensus management
        """
        self.meeting_id = meeting_id
        self.format_config = format_config
        self.members = members

        # Initialize managers
        self.context_manager = ContextManager(context_config or {})
        self.consensus_manager = ConsensusManager(consensus_config or {})
        self.health_monitor = HealthMonitor()

        # Initialize state
        self.state = MeetingState.INITIALIZED
        self.current_topic: Optional[str] = None
        self.discussion_history: List[Dict[str, Any]] = []
        self.action_items: List[Dict[str, Any]] = []
        self.decisions: List[Dict[str, Any]] = []

        # Meeting metadata
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.metrics: Dict[str, Any] = {}

    async def start(self) -> None:
        """Start the meeting.

        Initializes the meeting context, prepares members, and begins the meeting process.
        """
        self.state = MeetingState.STARTING
        self.start_time = datetime.now()

        # Initialize meeting context
        await self.context_manager.initialize_context(self.format_config)

        # Prepare members
        for member in self.members:
            self.health_monitor.register_member(member.name, member.role)

        self.state = MeetingState.IN_PROGRESS

    async def process_topic(
        self, topic: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a discussion topic.

        Args:
            topic: The topic to discuss
            context: Additional context for the discussion

        Returns:
            Dict containing discussion results and any decisions made
        """
        self.current_topic = topic
        discussion_context = await self.context_manager.get_context(topic, context)

        contributions = []
        for member in self.members:
            # Get member contribution
            contribution = await member.contribute_to_discussion(
                topic, discussion_context
            )
            contributions.append(contribution)

            # Update health metrics
            await self.health_monitor.update_member_metrics(member, contribution)

            # Update context with new contribution
            await self.context_manager.add_contribution(topic, contribution)

        # Process consensus if needed
        if self.format_config.get("requires_consensus", False):
            self.state = MeetingState.CONSENSUS_BUILDING
            consensus_result = await self.consensus_manager.process_contributions(
                topic, contributions, discussion_context
            )
            self.decisions.append(
                {
                    "topic": topic,
                    "consensus": consensus_result,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        self.state = MeetingState.IN_PROGRESS
        return {
            "topic": topic,
            "contributions": contributions,
            "context": discussion_context,
            "decisions": self.decisions[-1] if self.decisions else None,
        }

    async def conclude(self) -> Dict[str, Any]:
        """Conclude the meeting and generate summary information.

        Returns:
            Dict containing meeting summary and metrics
        """
        self.state = MeetingState.WRAPPING_UP

        # Generate meeting summary
        summary = await self.context_manager.generate_summary(self.discussion_history)

        # Collect final metrics
        self.metrics = {
            "duration": (datetime.now() - self.start_time).total_seconds(),
            "topics_covered": len(self.discussion_history),
            "decisions_made": len(self.decisions),
            "action_items": len(self.action_items),
            "member_metrics": await self.health_monitor.get_meeting_metrics(),
            "consensus_metrics": self.consensus_manager.get_metrics(),
        }

        self.state = MeetingState.CONCLUDED
        self.end_time = datetime.now()

        return {
            "summary": summary,
            "decisions": self.decisions,
            "action_items": self.action_items,
            "metrics": self.metrics,
        }

    async def add_action_item(
        self, description: str, assignee: str, due_date: Optional[str] = None
    ) -> None:
        """Add an action item to the meeting.

        Args:
            description: Description of the action item
            assignee: Member assigned to the action item
            due_date: Optional due date for the action item
        """
        self.action_items.append(
            {
                "description": description,
                "assignee": assignee,
                "due_date": due_date,
                "status": "pending",
                "created_at": datetime.now().isoformat(),
            }
        )

    def get_state(self) -> Dict[str, Any]:
        """Get the current meeting state.

        Returns:
            Dict containing current meeting state information
        """
        return {
            "state": self.state.value,
            "current_topic": self.current_topic,
            "member_count": len(self.members),
            "topics_covered": len(self.discussion_history),
            "decisions_made": len(self.decisions),
            "action_items": len(self.action_items),
            "duration": (
                (datetime.now() - self.start_time).total_seconds()
                if self.start_time
                else 0
            ),
        }

    async def pause(self) -> None:
        """Pause the meeting, saving current state."""
        self.state = MeetingState.PAUSED
        await self.context_manager.save_state()
        await self.consensus_manager.save_state()

    async def resume(self) -> None:
        """Resume a paused meeting."""
        if self.state != MeetingState.PAUSED:
            raise ValueError("Can only resume a paused meeting")

        await self.context_manager.restore_state()
        await self.consensus_manager.restore_state()
        self.state = MeetingState.IN_PROGRESS

    async def handle_error(self, error: Exception) -> None:
        """Handle meeting errors gracefully.

        Args:
            error: The error that occurred
        """
        self.state = MeetingState.ERROR
        # Log error and notify members
        # Attempt recovery or graceful degradation
        # Consider implementing retry logic or fallback mechanisms
