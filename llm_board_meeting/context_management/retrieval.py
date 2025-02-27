# llm_board_meeting/context_management/retrieval.py

"""
Retrieval system for the Context Management System.

This module implements efficient retrieval of context information using
semantic search and other retrieval methods.
"""

from typing import Dict, List, Optional, Set
from datetime import datetime

from llm_board_meeting.context_management.entry import ContextEntry
from llm_board_meeting.context_management.layers import ContextLayer


class RetrievalSystem:
    """Handles efficient retrieval of context information."""

    def search(
        self,
        query: str,
        context_layers: Dict[str, ContextLayer],
        target_layers: Optional[List[str]] = None,
    ) -> List[ContextEntry]:
        """Search for relevant context entries.

        Args:
            query: The search query.
            context_layers: Dict mapping layer names to layers.
            target_layers: Optional list of layers to search in.

        Returns:
            List of relevant context entries.
        """
        results = []
        layers_to_search = (
            target_layers if target_layers is not None else context_layers.keys()
        )

        for layer_name in layers_to_search:
            layer = context_layers[layer_name]
            relevant_entries = self._search_layer(query, layer)
            results.extend(relevant_entries)

        return sorted(results, key=lambda x: x.importance, reverse=True)

    def search_by_topic(
        self,
        topic: str,
        context_layers: Dict[str, ContextLayer],
        target_layers: Optional[List[str]] = None,
    ) -> List[ContextEntry]:
        """Search for entries related to a specific topic.

        Args:
            topic: The topic to search for.
            context_layers: Dict mapping layer names to layers.
            target_layers: Optional list of layers to search in.

        Returns:
            List of relevant entries.
        """
        results = []
        layers_to_search = (
            target_layers if target_layers is not None else context_layers.keys()
        )

        for layer_name in layers_to_search:
            layer = context_layers[layer_name]
            results.extend(layer.get_entries_by_topic(topic))

        return sorted(results, key=lambda x: x.importance, reverse=True)

    def search_by_timeframe(
        self,
        context_layers: Dict[str, ContextLayer],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        target_layers: Optional[List[str]] = None,
    ) -> List[ContextEntry]:
        """Search for entries within a specific timeframe.

        Args:
            context_layers: Dict mapping layer names to layers.
            start_time: Optional start time filter.
            end_time: Optional end time filter.
            target_layers: Optional list of layers to search in.

        Returns:
            List of relevant entries.
        """
        results = []
        layers_to_search = (
            target_layers if target_layers is not None else context_layers.keys()
        )

        for layer_name in layers_to_search:
            layer = context_layers[layer_name]
            results.extend(layer.get_entries(start_time, end_time))

        return sorted(results, key=lambda x: x.timestamp, reverse=True)

    def _search_layer(self, query: str, layer: ContextLayer) -> List[ContextEntry]:
        """Search within a specific context layer.

        Args:
            query: The search query.
            layer: The layer to search in.

        Returns:
            List of relevant entries from the layer.
        """
        relevant_entries = []
        query_keywords = self._extract_search_keywords(query)

        for entry in layer.entries:
            # Calculate relevance score based on multiple factors
            relevance_score = self._calculate_relevance(entry, query_keywords)

            if relevance_score > 0.3:  # Minimum relevance threshold
                entry.metadata["search_relevance"] = relevance_score
                relevant_entries.append(entry)

        return sorted(
            relevant_entries,
            key=lambda x: (x.metadata["search_relevance"], x.importance),
            reverse=True,
        )

    def _extract_search_keywords(self, query: str) -> Set[str]:
        """Extract keywords from search query.

        Args:
            query: The search query.

        Returns:
            Set of keywords.
        """
        # Simple keyword extraction (in practice, use NLP library)
        words = query.lower().split()
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to"}
        return {word for word in words if word not in stopwords and len(word) > 3}

    def _calculate_relevance(
        self, entry: ContextEntry, query_keywords: Set[str]
    ) -> float:
        """Calculate relevance score for an entry.

        Args:
            entry: The entry to evaluate.
            query_keywords: Keywords from the search query.

        Returns:
            Relevance score between 0 and 1.
        """
        # Get entry keywords
        entry_keywords = set(entry.metadata.get("keywords", []))
        if not entry_keywords:
            entry_keywords = self._extract_search_keywords(entry.content)

        # Calculate keyword overlap
        keyword_overlap = len(query_keywords & entry_keywords)
        if not keyword_overlap:
            return 0.0

        # Base score from keyword overlap
        base_score = keyword_overlap / len(query_keywords)

        # Adjust score based on factors
        recency_factor = self._calculate_recency_factor(entry)
        importance_factor = entry.importance

        # Combine factors (weights can be adjusted)
        final_score = base_score * 0.5 + recency_factor * 0.3 + importance_factor * 0.2

        return min(1.0, final_score)

    def _calculate_recency_factor(self, entry: ContextEntry) -> float:
        """Calculate recency factor for relevance scoring.

        Args:
            entry: The entry to evaluate.

        Returns:
            Recency factor between 0 and 1.
        """
        age_hours = (datetime.now() - entry.timestamp).total_seconds() / 3600
        # Decay factor: 0.9 per hour, minimum 0.1
        return max(0.1, 1 - (0.1 * age_hours))
