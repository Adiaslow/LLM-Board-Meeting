# llm_board_meeting/context_management/entry.py

"""
Context Entry module for the LLM Board Meeting system.

This module defines the fundamental unit of context management - the ContextEntry class.
Context entries represent discrete pieces of information that flow through the context
management system's layers, from active discussion to persistent knowledge.

Key Features:
- Structured representation of context information
- Metadata tracking for entry lifecycle
- Importance scoring and promotion logic
- Source attribution and versioning
- Temporal tracking and aging mechanisms

Each context entry maintains:
1. Core content and metadata
2. Temporal information (creation, modification, access times)
3. Importance metrics for promotion decisions
4. Source tracking for attribution
5. Version history for content evolution
6. Relationships to other entries

The module supports:
- Dynamic importance calculation
- Automatic metadata enrichment
- Content validation and sanitization
- Entry lifecycle management
- Relationship tracking between entries

Example:
    ```python
    entry = ContextEntry(
        content="Key decision on architecture",
        source="board_discussion",
        importance=0.8,
        metadata={
            "topic": "technical",
            "decision_type": "architecture",
            "stakeholders": ["tech_lead", "architect"]
        }
    )
    ```

This module is central to the context management system, providing the basic
building blocks for maintaining conversation history and knowledge persistence
while respecting token limits and relevance criteria.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class ContextEntry:
    """Data class representing a single context entry.

    Attributes:
        content: The actual content of the entry.
        timestamp: When the entry was created.
        source: Source of the entry (e.g., board member name).
        importance: Importance score for retention decisions.
        metadata: Additional metadata about the entry.
    """

    content: str
    timestamp: datetime
    source: str
    importance: float
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert the context entry to a dictionary format.

        Returns:
            Dict containing the entry's data in a serializable format.
        """
        return {
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "importance": self.importance,
            "metadata": self.metadata,
        }
