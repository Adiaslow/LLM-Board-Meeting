# llm_board_meeting/consensus_management/manager.py

"""
Consensus Manager implementation for the LLM Board Meeting system.

This module provides the core functionality for managing consensus building
processes, including strategy selection, entry processing, and metrics tracking.
"""

from typing import Any, Dict, List, Optional, Sequence, Type
from datetime import datetime

from llm_board_meeting.consensus_management.models import (
    ConsensusEntry,
    ConsensusConfig,
)
from llm_board_meeting.consensus_management.strategies import (
    ConsensusStrategy,
    VotingBasedStrategy,
    DiscussionBasedStrategy,
    HybridStrategy,
)
from llm_board_meeting.core.board_member import BoardMember


class ConsensusManager:
    """Manages consensus building processes in board meetings."""

    def __init__(self, config: ConsensusConfig) -> None:
        """Initialize ConsensusManager.

        Args:
            config: Configuration for consensus management.
        """
        self.config = config
        self.active_entries: List[ConsensusEntry] = []
        self.archived_entries: List[ConsensusEntry] = []
        self.metrics = {
            "total_entries": 0,
            "successful_consensus": 0,
            "failed_consensus": 0,
            "average_rounds": 0.0,
        }

        # Initialize strategies
        self.strategies = {
            "voting": VotingBasedStrategy(config),
            "discussion": DiscussionBasedStrategy(config),
            "hybrid": HybridStrategy(config),
        }

    async def process_entry(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, Any]:
        """Process a consensus entry through the appropriate strategy.

        Args:
            entry: The consensus entry to process.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing process results.
        """
        if entry not in self.active_entries:
            self.active_entries.append(entry)

        strategy = self._select_strategy(entry)
        result = await strategy.process(entry, board_members)

        self._update_metrics(result)

        if result["status"] in ["achieved", "failed"]:
            self.archive_entry(entry)

        return result

    def _select_strategy(self, entry: ConsensusEntry) -> ConsensusStrategy:
        """Select appropriate consensus strategy based on entry characteristics.

        Args:
            entry: The consensus entry to process.

        Returns:
            Selected consensus strategy.
        """
        if entry.consensus_type != "auto":
            return self.strategies.get(entry.consensus_type, self.strategies["hybrid"])

        # For auto selection, use heuristics
        if entry.metadata.get("complexity", 0) > 0.7:
            return self.strategies["discussion"]
        elif entry.metadata.get("time_sensitive", False):
            return self.strategies["voting"]
        else:
            return self.strategies["hybrid"]

    def _update_metrics(self, result: Dict[str, Any]) -> None:
        """Update consensus metrics based on process result.

        Args:
            result: Result from consensus process.
        """
        self.metrics["total_entries"] += 1
        if result["status"] == "achieved":
            self.metrics["successful_consensus"] += 1
        elif result["status"] == "failed":
            self.metrics["failed_consensus"] += 1

        if "rounds" in result:
            total_rounds = (
                self.metrics["average_rounds"] * (self.metrics["total_entries"] - 1)
                + result["rounds"]
            )
            self.metrics["average_rounds"] = (
                total_rounds / self.metrics["total_entries"]
            )

    def archive_entry(self, entry: ConsensusEntry) -> None:
        """Archive a completed consensus entry.

        Args:
            entry: The consensus entry to archive.
        """
        if entry in self.active_entries:
            self.active_entries.remove(entry)
            self.archived_entries.append(entry)

    def get_active_entries(self) -> List[ConsensusEntry]:
        """Get list of active consensus entries.

        Returns:
            List of active consensus entries.
        """
        return self.active_entries

    def get_entry_history(self, topic: str) -> List[ConsensusEntry]:
        """Get history of consensus entries for a topic.

        Args:
            topic: The topic to get history for.

        Returns:
            List of consensus entries for the topic.
        """
        return [
            entry
            for entry in self.active_entries + self.archived_entries
            if entry.topic == topic
        ]

    def get_consensus_summary(self) -> Dict[str, Any]:
        """Get summary of consensus management activities.

        Returns:
            Dict containing consensus summary.
        """
        return {
            "metrics": self.metrics,
            "active_entries": len(self.active_entries),
            "archived_entries": len(self.archived_entries),
        }

    async def process_contributions(
        self,
        topic: str,
        contributions: List[Dict[str, Any]],
        context: Dict[str, Any],
        board_members: Sequence[BoardMember],
    ) -> Dict[str, Any]:
        """Process multiple contributions to build consensus.

        Args:
            topic: The topic being discussed.
            contributions: List of contribution dictionaries from board members.
            context: Additional context for consensus building.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing consensus results.
        """
        # Create a new consensus entry for the contributions
        entry = ConsensusEntry(
            topic=topic,
            content={"contributions": contributions},
            source_role="system",
            metadata={
                "context": context,
                "contribution_count": len(contributions),
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Process the entry using the appropriate strategy
        result = await self.process_entry(entry, board_members)

        # Add contribution-specific metrics
        result["contribution_metrics"] = {
            "total_contributions": len(contributions),
            "contributing_roles": list(
                set(c.get("role") for c in contributions if "role" in c)
            ),
            "contribution_types": list(
                set(c.get("type") for c in contributions if "type" in c)
            ),
        }

        return result

    def get_metrics(self) -> Dict[str, Any]:
        """Get consensus management metrics.

        Returns:
            Dict containing metrics about consensus processes.
        """
        return {
            **self.metrics,
            "success_rate": (
                self.metrics["successful_consensus"] / self.metrics["total_entries"]
                if self.metrics["total_entries"] > 0
                else 0.0
            ),
            "active_processes": len(self.active_entries),
            "archived_processes": len(self.archived_entries),
            "last_updated": datetime.now().isoformat(),
        }
