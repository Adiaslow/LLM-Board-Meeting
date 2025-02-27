# llm_board_meeting/context_management/memory.py

"""
Memory management for the Context Management System.

This module handles transitions between context layers and enforces retention
policies, following the Single Responsibility Principle.
"""

from typing import Dict, List, Any
from datetime import datetime

from llm_board_meeting.context_management.entry import ContextEntry
from llm_board_meeting.context_management.layers import ContextLayer


class MemoryManager:
    """Manages transitions between context layers and enforces retention policies."""

    def __init__(
        self,
        active_discussion: ContextLayer,
        key_points: ContextLayer,
        meeting_framework: ContextLayer,
        persistent_knowledge: ContextLayer,
    ) -> None:
        """Initialize the memory manager.

        Args:
            active_discussion: Active discussion layer.
            key_points: Key points layer.
            meeting_framework: Meeting framework layer.
            persistent_knowledge: Persistent knowledge layer.
        """
        self.active_discussion = active_discussion
        self.key_points = key_points
        self.meeting_framework = meeting_framework
        self.persistent_knowledge = persistent_knowledge

    def process_new_entry(self, entry: ContextEntry, layer: str) -> None:
        """Process a new entry and manage transitions.

        Args:
            entry: The new context entry.
            layer: The layer the entry was added to.
        """
        if layer == "active_discussion":
            self._check_for_key_points(entry)
        self._update_importance_scores()
        self._enforce_retention_policies()

    def process_promotion(self, entry: ContextEntry, target_layer: str) -> None:
        """Process the promotion of an entry to a higher layer.

        Args:
            entry: The entry being promoted.
            target_layer: The layer to promote to.
        """
        self._validate_promotion(entry, target_layer)
        self._update_references(entry, target_layer)
        self._enforce_retention_policies()

    def process_framework_update(self, entry: ContextEntry) -> None:
        """Process an update to the meeting framework.

        Args:
            entry: The new framework entry.
        """
        self._update_framework_references(entry)
        self._enforce_retention_policies()

    def process_knowledge_addition(self, entry: ContextEntry) -> None:
        """Process the addition of persistent knowledge.

        Args:
            entry: The new knowledge entry.
        """
        self._index_knowledge(entry)
        self._update_related_entries(entry)
        self._enforce_retention_policies()

    def _check_for_key_points(self, entry: ContextEntry) -> None:
        """Check if an active discussion entry should be promoted to key points.

        Args:
            entry: The entry to evaluate for promotion.
        """
        # Define promotion criteria
        importance_threshold = 0.7
        key_terms = ["decision", "action item", "conclusion", "agreement", "milestone"]

        # Check importance score
        if entry.importance >= importance_threshold:
            self.process_promotion(entry, "key_points")
            return

        # Check for key terms in content
        if any(term.lower() in entry.content.lower() for term in key_terms):
            entry.importance = 0.8  # Boost importance for key terms
            self.process_promotion(entry, "key_points")
            return

        # Check metadata flags
        if entry.metadata.get("is_key_point", False):
            self.process_promotion(entry, "key_points")

    def _update_importance_scores(self) -> None:
        """Update importance scores based on usage and relevance."""
        current_time = datetime.now()

        for layer in [
            self.active_discussion,
            self.key_points,
            self.meeting_framework,
            self.persistent_knowledge,
        ]:
            for entry in layer.entries:
                # Apply time decay (reduce importance by 10% per hour)
                time_diff = (current_time - entry.timestamp).total_seconds() / 3600
                time_factor = max(0.1, 1 - (0.1 * time_diff))

                # Consider reference count from metadata
                ref_count = entry.metadata.get("reference_count", 0)
                ref_factor = min(2.0, 1 + (0.1 * ref_count))

                # Consider user-defined importance
                user_importance = entry.metadata.get("user_importance", 1.0)

                # Calculate new importance score
                entry.importance = min(
                    1.0, entry.importance * time_factor * ref_factor * user_importance
                )

    def _enforce_retention_policies(self) -> None:
        """Enforce retention policies across all layers."""
        for layer in [
            self.active_discussion,
            self.key_points,
            self.meeting_framework,
            self.persistent_knowledge,
        ]:
            # Remove entries below importance threshold
            importance_threshold = 0.2
            layer.entries = [
                e for e in layer.entries if e.importance >= importance_threshold
            ]

            # Archive old entries (keep last 24 hours for active discussion)
            if layer == self.active_discussion:
                layer.clear_old_entries(max_age_hours=24)

            # Enforce maximum entries limit
            layer._enforce_limits()

    def _validate_promotion(self, entry: ContextEntry, target_layer: str) -> None:
        """Validate that an entry can be promoted to the target layer.

        Args:
            entry: The entry to promote.
            target_layer: The target layer for promotion.

        Raises:
            ValueError: If promotion criteria are not met.
        """
        if target_layer == "key_points":
            if entry.importance < 0.5:
                raise ValueError("Entry importance too low for promotion to key points")
        elif target_layer == "persistent_knowledge":
            if not entry.metadata.get("verified", False):
                raise ValueError(
                    "Entry must be verified for promotion to persistent knowledge"
                )
            if entry.importance < 0.8:
                raise ValueError("Entry importance too low for persistent knowledge")

    def _update_references(self, entry: ContextEntry, target_layer: str) -> None:
        """Update references when an entry is promoted.

        Args:
            entry: The promoted entry.
            target_layer: The layer the entry was promoted to.
        """
        # Add reference to original location
        entry.metadata["promoted_from"] = entry.metadata.get("current_layer", "unknown")
        entry.metadata["current_layer"] = target_layer
        entry.metadata["promotion_time"] = datetime.now()

        # Update reference counts
        entry.metadata["reference_count"] = entry.metadata.get("reference_count", 0) + 1

    def _update_framework_references(self, entry: ContextEntry) -> None:
        """Update references when the framework is updated.

        Args:
            entry: The new framework entry.
        """
        # Tag entries related to current framework
        framework_topics = entry.metadata.get("topics", [])

        for layer in [self.active_discussion, self.key_points]:
            for existing_entry in layer.entries:
                if any(
                    topic in existing_entry.metadata.get("topics", [])
                    for topic in framework_topics
                ):
                    existing_entry.metadata["framework_relevant"] = True
                    existing_entry.importance *= 1.2  # Boost importance

    def _index_knowledge(self, entry: ContextEntry) -> None:
        """Index new knowledge for efficient retrieval.

        Args:
            entry: The new knowledge entry.
        """
        # Extract keywords for indexing
        keywords = self._extract_keywords(entry.content)
        entry.metadata["keywords"] = keywords

        # Add to topic index
        topics = entry.metadata.get("topics", [])
        for topic in topics:
            entry.metadata[f"topic_{topic}_indexed"] = True

        # Update timestamp index
        entry.metadata["indexed_at"] = datetime.now()

    def _update_related_entries(self, entry: ContextEntry) -> None:
        """Update entries related to new knowledge.

        Args:
            entry: The new knowledge entry.
        """
        # Find related entries based on keywords and topics
        keywords = entry.metadata.get("keywords", [])
        topics = entry.metadata.get("topics", [])

        for layer in [
            self.active_discussion,
            self.key_points,
            self.meeting_framework,
            self.persistent_knowledge,
        ]:
            for existing_entry in layer.entries:
                existing_keywords = existing_entry.metadata.get("keywords", [])
                existing_topics = existing_entry.metadata.get("topics", [])

                # Calculate relationship strength
                keyword_overlap = len(set(keywords) & set(existing_keywords))
                topic_overlap = len(set(topics) & set(existing_topics))

                if keyword_overlap > 0 or topic_overlap > 0:
                    # Update relationship metadata
                    existing_entry.metadata["related_entries"] = (
                        existing_entry.metadata.get("related_entries", [])
                        + [entry.timestamp]
                    )
                    existing_entry.metadata["relationship_strength"] = (
                        keyword_overlap * 0.6
                    ) + (topic_overlap * 0.4)

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content for indexing.

        Args:
            content: The content to extract keywords from.

        Returns:
            List of extracted keywords.
        """
        # Simple keyword extraction (in practice, use NLP library)
        words = content.lower().split()
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to"}
        keywords = [word for word in words if word not in stopwords and len(word) > 3]
        return list(set(keywords))  # Remove duplicates
