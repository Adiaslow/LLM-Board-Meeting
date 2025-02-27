# llm_board_meeting/context_management/summarization.py

"""
Summarization engine for the Context Management System.

This module implements the summarization functionality for generating concise
representations of context information across different layers.
"""

from typing import Dict, List, Set, Optional
from datetime import datetime, timedelta
from collections import Counter

from llm_board_meeting.context_management.entry import ContextEntry
from llm_board_meeting.context_management.layers import ContextLayer


class SummarizationEngine:
    """Handles generation of concise context representations."""

    def create_layer_summary(
        self,
        layer: ContextLayer,
        time_window: Optional[timedelta] = None,
        min_importance: float = 0.0,
    ) -> str:
        """Create a summary for a specific context layer.

        Args:
            layer: The layer to summarize.
            time_window: Optional time window to limit entries.
            min_importance: Minimum importance score for included entries.

        Returns:
            A formatted summary string.
        """
        # Filter entries by time and importance
        entries = layer.entries
        if time_window:
            cutoff_time = datetime.now() - time_window
            entries = [e for e in entries if e.timestamp >= cutoff_time]
        entries = [e for e in entries if e.importance >= min_importance]

        if not entries:
            return "No significant entries found in the specified timeframe."

        # Extract themes and create summary
        themes = self._extract_themes(entries)
        return self._create_summary(entries, themes)

    def create_multi_layer_summary(
        self,
        context_layers: Dict[str, ContextLayer],
        target_layers: Optional[List[str]] = None,
        time_window: Optional[timedelta] = None,
    ) -> str:
        """Create a summary spanning multiple context layers.

        Args:
            context_layers: Dict mapping layer names to layers.
            target_layers: Optional list of layers to summarize.
            time_window: Optional time window to limit entries.

        Returns:
            A formatted multi-layer summary string.
        """
        layers_to_summarize = (
            target_layers if target_layers is not None else context_layers.keys()
        )

        summaries = []
        for layer_name in layers_to_summarize:
            layer = context_layers[layer_name]
            # Adjust minimum importance based on layer type
            min_importance = {
                "active_discussion": 0.3,
                "key_points": 0.5,
                "meeting_framework": 0.0,
                "persistent_knowledge": 0.7,
            }.get(layer_name, 0.0)

            layer_summary = self.create_layer_summary(
                layer, time_window, min_importance=min_importance
            )
            if layer_summary:
                summaries.append(
                    f"## {layer_name.replace('_', ' ').title()}\n{layer_summary}"
                )

        return (
            "\n\n".join(summaries)
            if summaries
            else "No significant content to summarize."
        )

    def create_topic_summary(
        self,
        topic: str,
        context_layers: Dict[str, ContextLayer],
        target_layers: Optional[List[str]] = None,
    ) -> str:
        """Create a summary focused on a specific topic.

        Args:
            topic: The topic to summarize.
            context_layers: Dict mapping layer names to layers.
            target_layers: Optional list of layers to include.

        Returns:
            A topic-focused summary string.
        """
        layers_to_search = (
            target_layers if target_layers is not None else context_layers.keys()
        )

        # Collect topic-related entries from all layers
        topic_entries = []
        for layer_name in layers_to_search:
            layer = context_layers[layer_name]
            entries = layer.get_entries_by_topic(topic)
            topic_entries.extend(entries)

        if not topic_entries:
            return f"No entries found for topic: {topic}"

        # Sort by importance and recency
        topic_entries.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)

        # Extract themes and create summary
        themes = self._extract_themes(topic_entries)
        summary = self._create_summary(topic_entries, themes)

        return f"# Topic Summary: {topic}\n\n{summary}"

    def _extract_themes(self, entries: List[ContextEntry]) -> List[str]:
        """Extract key themes from a list of context entries.

        Args:
            entries: List of entries to analyze.

        Returns:
            List of identified themes.
        """
        # Collect all keywords and explicit themes
        keywords = []
        explicit_themes = set()

        for entry in entries:
            # Get keywords from content or metadata
            entry_keywords = entry.metadata.get("keywords", [])
            if not entry_keywords:
                entry_keywords = self._extract_keywords(entry.content)
            keywords.extend(entry_keywords)

            # Get explicit themes from metadata
            themes = entry.metadata.get("themes", [])
            explicit_themes.update(themes)

        # Count keyword frequencies
        keyword_counts = Counter(keywords)

        # Identify top themes from keywords (excluding those already explicit)
        keyword_themes = {
            word
            for word, count in keyword_counts.most_common(5)
            if count >= 2 and word not in explicit_themes
        }

        # Combine explicit themes and keyword-based themes
        return list(explicit_themes) + list(keyword_themes)

    def _create_summary(self, entries: List[ContextEntry], themes: List[str]) -> str:
        """Generate a textual summary of entries.

        Args:
            entries: List of entries to summarize.
            themes: List of identified themes.

        Returns:
            Formatted summary string.
        """
        # Time context
        time_range = self._get_time_range(entries)

        # Contributors
        contributors = self._get_contributors(entries)

        # Key themes section
        themes_section = "### Key Themes\n" + "\n".join(
            f"- {theme}" for theme in themes
        )

        # Key points from most important entries
        important_entries = sorted(entries, key=lambda x: x.importance, reverse=True)[
            :5
        ]
        key_points = []
        for entry in important_entries:
            if entry.importance >= 0.5:  # Only include significant points
                point = entry.content.strip()
                if len(point) > 100:  # Truncate long entries
                    point = point[:97] + "..."
                key_points.append(f"- {point}")

        key_points_section = "### Key Points\n" + "\n".join(key_points)

        # Combine sections
        summary = f"""### Time Context
{time_range}

### Contributors
{contributors}

{themes_section}

{key_points_section}"""

        return summary

    def _get_time_range(self, entries: List[ContextEntry]) -> str:
        """Get a formatted time range string.

        Args:
            entries: List of entries to analyze.

        Returns:
            Formatted time range string.
        """
        if not entries:
            return "No entries"

        start_time = min(e.timestamp for e in entries)
        end_time = max(e.timestamp for e in entries)

        if start_time.date() == end_time.date():
            return f"Single day: {start_time.strftime('%Y-%m-%d')}"
        else:
            return f"From {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}"

    def _get_contributors(self, entries: List[ContextEntry]) -> str:
        """Get a formatted list of contributors.

        Args:
            entries: List of entries to analyze.

        Returns:
            Formatted contributors string.
        """
        contributors = Counter(entry.source for entry in entries)
        return "\n".join(
            f"- {source}: {count} contributions"
            for source, count in contributors.most_common()
        )

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract keywords from content.

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
