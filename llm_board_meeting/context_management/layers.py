# llm_board_meeting/context_management/layers.py

"""
Layer management for the Context Management System.

This module implements the layer management functionality, handling entry storage,
retention policies, and layer-specific operations.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from llm_board_meeting.context_management.entry import ContextEntry
from llm_board_meeting.context_management.config import LayerConfig


class ContextLayer:
    """Base class for context layers in the hierarchy.

    Each layer manages a specific type of context information with its own
    retention and summarization policies.
    """

    def __init__(self, config: LayerConfig) -> None:
        """Initialize a context layer.

        Args:
            config: Configuration for the layer.
        """
        self.config = config
        self.entries: List[ContextEntry] = []

    def add_entry(self, entry: ContextEntry) -> None:
        """Add a new entry to the layer.

        Args:
            entry: The context entry to add.
        """
        self.entries.append(entry)
        self._enforce_limits()

    def get_entries(
        self, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None
    ) -> List[ContextEntry]:
        """Get entries within a time range.

        Args:
            start_time: Optional start time filter.
            end_time: Optional end time filter.

        Returns:
            List of entries within the time range.
        """
        if not start_time and not end_time:
            return self.entries

        filtered_entries = self.entries
        if start_time:
            filtered_entries = [
                e for e in filtered_entries if e.timestamp >= start_time
            ]
        if end_time:
            filtered_entries = [e for e in filtered_entries if e.timestamp <= end_time]
        return filtered_entries

    def get_entries_by_topic(self, topic: str) -> List[ContextEntry]:
        """Get entries related to a specific topic.

        Args:
            topic: The topic to filter by.

        Returns:
            List of entries related to the topic.
        """
        topic_lower = topic.lower()
        return [
            e
            for e in self.entries
            if (
                # Check direct topic match
                e.metadata.get("topic", "").lower() == topic_lower
                # Check topics list
                or topic_lower in [t.lower() for t in e.metadata.get("topics", [])]
                # Check topic in content
                or topic_lower in e.content.lower()
            )
        ]

    def get_entries_by_source(self, source: str) -> List[ContextEntry]:
        """Get entries from a specific source.

        Args:
            source: The source to filter by.

        Returns:
            List of entries from the source.
        """
        return [e for e in self.entries if e.source.lower() == source.lower()]

    def _enforce_limits(self) -> None:
        """Enforce maximum entry and token limits.

        This method removes oldest/least important entries when limits are exceeded.
        """
        if self.config.retention_policy == "importance":
            # Sort by importance and timestamp
            self.entries.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
        else:  # time-based retention
            # Sort by timestamp only
            self.entries.sort(key=lambda x: x.timestamp, reverse=True)

        # Truncate to max entries
        if len(self.entries) > self.config.max_entries:
            self.entries = self.entries[: self.config.max_entries]

    def clear_old_entries(self, max_age_hours: float) -> None:
        """Remove entries older than specified age.

        Args:
            max_age_hours: Maximum age of entries in hours.
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        self.entries = [e for e in self.entries if e.timestamp >= cutoff_time]

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the layer.

        Returns:
            Dict containing layer statistics.
        """
        if not self.entries:
            return {
                "total_entries": 0,
                "avg_importance": 0.0,
                "oldest_entry": None,
                "newest_entry": None,
                "sources": [],
            }

        return {
            "total_entries": len(self.entries),
            "avg_importance": sum(e.importance for e in self.entries)
            / len(self.entries),
            "oldest_entry": min(e.timestamp for e in self.entries),
            "newest_entry": max(e.timestamp for e in self.entries),
            "sources": list(set(e.source for e in self.entries)),
        }
