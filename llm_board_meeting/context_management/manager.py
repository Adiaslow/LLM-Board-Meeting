# llm_board_meeting/context_management/manager.py

"""
Main entry point for the Context Management System.

This module integrates all components of the context management system,
providing a unified interface for managing context across different layers
and functionalities.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

from llm_board_meeting.context_management.entry import ContextEntry
from llm_board_meeting.context_management.config import LayerConfig
from llm_board_meeting.context_management.layers import ContextLayer
from llm_board_meeting.context_management.memory import MemoryManager
from llm_board_meeting.context_management.retrieval import RetrievalSystem
from llm_board_meeting.context_management.summarization import SummarizationEngine


class ContextManager:
    """Main class for managing the Context Management System.

    This class integrates all components (MemoryManager, RetrievalSystem,
    SummarizationEngine) and provides a unified interface for context management.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the context manager.

        Args:
            config: Optional configuration dictionary with layer settings.
                   If a single integer is provided, it's treated as max_history
                   for the active discussion layer.
        """
        # Handle the case where config is a simple integer (max_history)
        if isinstance(config, dict) and len(config) == 1 and "max_history" in config:
            max_history = config["max_history"]
            config = {
                "active_discussion": {
                    "max_entries": max_history,
                    "max_tokens": max_history
                    * 100,  # Reasonable token estimate per entry
                    "retention_policy": "time",
                    "summarization_policy": "recent_first",
                }
            }

        # Initialize default configurations if none provided
        self.config = config or {
            "active_discussion": {
                "max_entries": 50,
                "max_tokens": 8000,
                "retention_policy": "time",
                "summarization_policy": "recent_first",
            },
            "key_points": {
                "max_entries": 100,
                "max_tokens": 12000,
                "retention_policy": "importance",
                "summarization_policy": "importance_first",
            },
            "meeting_framework": {
                "max_entries": 20,
                "max_tokens": 4000,
                "retention_policy": "manual",
                "summarization_policy": "structured",
            },
            "persistent_knowledge": {
                "max_entries": 200,
                "max_tokens": 16000,
                "retention_policy": "importance",
                "summarization_policy": "importance_first",
            },
        }

        # Initialize context layers
        self.layers: Dict[str, ContextLayer] = {}
        for layer_name, layer_config in self.config.items():
            # Create a proper LayerConfig object with all required fields
            config_obj = LayerConfig(
                max_entries=layer_config["max_entries"],
                max_tokens=layer_config["max_tokens"],
                retention_policy=layer_config["retention_policy"],
                summarization_policy=layer_config["summarization_policy"],
            )
            self.layers[layer_name] = ContextLayer(config_obj)

        # Initialize components
        self.memory_manager = MemoryManager(
            active_discussion=self.layers.get(
                "active_discussion",
                ContextLayer(
                    LayerConfig(
                        max_entries=50,
                        max_tokens=8000,
                        retention_policy="time",
                        summarization_policy="recent_first",
                    )
                ),
            ),
            key_points=self.layers.get(
                "key_points",
                ContextLayer(
                    LayerConfig(
                        max_entries=100,
                        max_tokens=12000,
                        retention_policy="importance",
                        summarization_policy="importance_first",
                    )
                ),
            ),
            meeting_framework=self.layers.get(
                "meeting_framework",
                ContextLayer(
                    LayerConfig(
                        max_entries=20,
                        max_tokens=4000,
                        retention_policy="manual",
                        summarization_policy="structured",
                    )
                ),
            ),
            persistent_knowledge=self.layers.get(
                "persistent_knowledge",
                ContextLayer(
                    LayerConfig(
                        max_entries=200,
                        max_tokens=16000,
                        retention_policy="importance",
                        summarization_policy="importance_first",
                    )
                ),
            ),
        )
        self.retrieval_system = RetrievalSystem()
        self.summarization_engine = SummarizationEngine()

    async def initialize_context(self, format_config: Dict[str, Any]) -> None:
        """Initialize the context with meeting format configuration.

        Args:
            format_config: Meeting format configuration dictionary.
        """
        # Add format configuration to meeting framework layer
        self.update_framework(
            content="Meeting Format Configuration",
            metadata={
                "type": "format_config",
                "config": format_config,
                "timestamp": datetime.now().isoformat(),
            },
        )

        # Initialize active discussion with format info
        self.add_entry(
            content=f"Meeting Format: {format_config.get('format', 'standard')}",
            source="system",
            layer="active_discussion",
            metadata={
                "type": "format_info",
                "importance": 0.8,
                "config": format_config,
            },
        )

        # Add any topics to key points
        if topics := format_config.get("topics", []):
            self.add_entry(
                content=f"Meeting Topics: {', '.join(topics)}",
                source="system",
                layer="key_points",
                metadata={
                    "type": "topics",
                    "importance": 0.9,
                    "topics": topics,
                },
            )

    def add_entry(
        self, content: str, source: str, layer: str, metadata: Optional[Dict] = None
    ) -> None:
        """Add a new entry to a context layer.

        Args:
            content: The content of the entry.
            source: The source of the entry (e.g., board member role).
            layer: The target layer for the entry.
            metadata: Optional metadata for the entry.

        Raises:
            ValueError: If the specified layer doesn't exist.
        """
        if layer not in self.layers:
            raise ValueError(f"Invalid layer: {layer}")

        entry = ContextEntry(
            content=content,
            source=source,
            timestamp=datetime.now(),
            importance=metadata.get("importance", 0.5) if metadata else 0.5,
            metadata=metadata or {},
        )

        # Add entry to layer
        self.layers[layer].add_entry(entry)

        # Process the new entry
        self.memory_manager.process_new_entry(entry, layer)

    def promote_entry(self, entry: ContextEntry, target_layer: str) -> None:
        """Promote an entry to a higher context layer.

        Args:
            entry: The entry to promote.
            target_layer: The target layer for promotion.

        Raises:
            ValueError: If promotion criteria are not met.
        """
        self.memory_manager.process_promotion(entry, target_layer)

    def update_framework(self, content: str, metadata: Optional[Dict] = None) -> None:
        """Update the meeting framework.

        Args:
            content: The framework update content.
            metadata: Optional metadata for the framework entry.
        """
        entry = ContextEntry(
            content=content,
            source="system",
            timestamp=datetime.now(),
            importance=1.0,  # Framework entries are always important
            metadata=metadata or {},
        )
        self.layers["meeting_framework"].add_entry(entry)
        self.memory_manager.process_framework_update(entry)

    def add_knowledge(self, content: str, metadata: Optional[Dict] = None) -> None:
        """Add an entry to persistent knowledge.

        Args:
            content: The knowledge content to add.
            metadata: Optional metadata for the knowledge entry.
        """
        entry = ContextEntry(
            content=content,
            source="system",
            timestamp=datetime.now(),
            importance=0.8,  # Knowledge entries start with high importance
            metadata=metadata or {"verified": True},  # Knowledge entries are verified
        )
        self.layers["persistent_knowledge"].add_entry(entry)
        self.memory_manager.process_knowledge_addition(entry)

    def search_context(
        self,
        query: str,
        target_layers: Optional[List[str]] = None,
        min_relevance: float = 0.3,
    ) -> List[ContextEntry]:
        """Search for relevant context entries.

        Args:
            query: The search query.
            target_layers: Optional list of layers to search in.
            min_relevance: Minimum relevance score for results.

        Returns:
            List of relevant context entries.
        """
        results = self.retrieval_system.search(
            query, self.layers, target_layers=target_layers
        )
        return [
            r for r in results if r.metadata.get("search_relevance", 0) >= min_relevance
        ]

    def search_by_topic(
        self, topic: str, target_layers: Optional[List[str]] = None
    ) -> List[ContextEntry]:
        """Search for entries related to a specific topic.

        Args:
            topic: The topic to search for.
            target_layers: Optional list of layers to search in.

        Returns:
            List of topic-related entries.
        """
        return self.retrieval_system.search_by_topic(
            topic, self.layers, target_layers=target_layers
        )

    def get_layer_summary(
        self,
        layer_name: str,
        time_window: Optional[timedelta] = None,
        min_importance: float = 0.0,
    ) -> str:
        """Get a summary for a specific layer.

        Args:
            layer_name: The name of the layer to summarize.
            time_window: Optional time window to limit entries.
            min_importance: Minimum importance score for included entries.

        Returns:
            A formatted summary string.

        Raises:
            ValueError: If the specified layer doesn't exist.
        """
        if layer_name not in self.layers:
            raise ValueError(f"Invalid layer: {layer_name}")

        return self.summarization_engine.create_layer_summary(
            self.layers[layer_name],
            time_window=time_window,
            min_importance=min_importance,
        )

    def get_multi_layer_summary(
        self,
        target_layers: Optional[List[str]] = None,
        time_window: Optional[timedelta] = None,
    ) -> str:
        """Get a summary spanning multiple layers.

        Args:
            target_layers: Optional list of layers to summarize.
            time_window: Optional time window to limit entries.

        Returns:
            A formatted multi-layer summary string.
        """
        return self.summarization_engine.create_multi_layer_summary(
            self.layers, target_layers=target_layers, time_window=time_window
        )

    def get_topic_summary(
        self, topic: str, target_layers: Optional[List[str]] = None
    ) -> str:
        """Get a summary focused on a specific topic.

        Args:
            topic: The topic to summarize.
            target_layers: Optional list of layers to include.

        Returns:
            A topic-focused summary string.
        """
        return self.summarization_engine.create_topic_summary(
            topic, self.layers, target_layers=target_layers
        )

    async def get_context(
        self, topic: str, additional_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Get context for a given topic, combining relevant entries with additional context.

        Args:
            topic: The topic to get context for.
            additional_context: Additional context to include.

        Returns:
            Dict containing combined context information.
        """
        # Search for relevant entries across all layers
        relevant_entries = self.search_by_topic(topic)

        # Get topic-specific summary
        topic_summary = self.get_topic_summary(topic)

        # Combine context from different sources
        context = {
            "topic": topic,
            "topic_summary": topic_summary,
            "relevant_entries": [entry.to_dict() for entry in relevant_entries],
            "framework": self.get_layer_summary("meeting_framework"),
            "key_points": self.get_layer_summary("key_points"),
            "additional_context": additional_context,
        }

        return context

    def get_layer_statistics(self, layer_name: str) -> Dict[str, Any]:
        """Get statistics for a specific layer.

        Args:
            layer_name: The name of the layer.

        Returns:
            Dictionary containing layer statistics.

        Raises:
            ValueError: If the specified layer doesn't exist.
        """
        if layer_name not in self.layers:
            raise ValueError(f"Invalid layer: {layer_name}")

        return self.layers[layer_name].get_statistics()

    def clear_old_entries(self, layer_name: str, max_age_hours: float) -> None:
        """Clear old entries from a layer.

        Args:
            layer_name: The name of the layer.
            max_age_hours: Maximum age of entries in hours.

        Raises:
            ValueError: If the specified layer doesn't exist.
        """
        if layer_name not in self.layers:
            raise ValueError(f"Invalid layer: {layer_name}")

        self.layers[layer_name].clear_old_entries(max_age_hours)

    async def add_contribution(self, topic: str, contribution: Dict[str, Any]) -> None:
        """Add a member's contribution to the context.

        Args:
            topic: The topic being discussed.
            contribution: The contribution data from a board member.
        """
        # Add to active discussion layer
        self.add_entry(
            content=contribution.get("content", ""),
            source=contribution.get("source", "unknown"),
            layer="active_discussion",
            metadata={
                "topic": topic,
                "type": contribution.get("type", "discussion"),
                "importance": contribution.get("importance", 0.5),
                "timestamp": datetime.now().isoformat(),
                "contribution_metadata": contribution.get("metadata", {}),
            },
        )

        # Check if contribution should be promoted to key points
        if contribution.get("importance", 0.5) >= 0.7 or contribution.get(
            "is_key_point", False
        ):
            self.add_entry(
                content=contribution.get("content", ""),
                source=contribution.get("source", "unknown"),
                layer="key_points",
                metadata={
                    "topic": topic,
                    "type": contribution.get("type", "key_point"),
                    "importance": max(0.7, contribution.get("importance", 0.7)),
                    "timestamp": datetime.now().isoformat(),
                    "contribution_metadata": contribution.get("metadata", {}),
                },
            )

    async def generate_summary(
        self, discussion_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate a comprehensive meeting summary from the discussion history.

        Args:
            discussion_history: List of discussion entries with their metadata.

        Returns:
            Dict containing the meeting summary with various components.
        """
        # Get summaries from each layer
        active_summary = self.get_layer_summary("active_discussion")
        key_points_summary = self.get_layer_summary("key_points")
        framework_summary = self.get_layer_summary("meeting_framework")
        knowledge_summary = self.get_layer_summary("persistent_knowledge")

        # Extract topics from discussion history
        topics = list(
            set(
                entry.get("topic", "")
                for entry in discussion_history
                if entry.get("topic")
            )
        )

        # Get topic-specific summaries
        topic_summaries = {topic: self.get_topic_summary(topic) for topic in topics}

        # Create multi-layer summary for overall context
        overall_summary = self.get_multi_layer_summary()

        return {
            "overall_summary": overall_summary,
            "layer_summaries": {
                "active_discussion": active_summary,
                "key_points": key_points_summary,
                "meeting_framework": framework_summary,
                "persistent_knowledge": knowledge_summary,
            },
            "topic_summaries": topic_summaries,
            "total_contributions": len(discussion_history),
            "topics_covered": topics,
            "timestamp": datetime.now().isoformat(),
        }
