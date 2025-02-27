# llm_board_meeting/context_management/__init__.py

"""
Context Management System for LLM Board Meeting.

This package provides a hierarchical approach to maintaining conversation history
within token limits, with support for different context layers, memory management,
retrieval, and summarization.
"""

from llm_board_meeting.context_management.entry import ContextEntry
from llm_board_meeting.context_management.config import LayerConfig
from llm_board_meeting.context_management.layers import ContextLayer
from llm_board_meeting.context_management.memory import MemoryManager
from llm_board_meeting.context_management.retrieval import RetrievalSystem
from llm_board_meeting.context_management.summarization import SummarizationEngine
from llm_board_meeting.context_management.manager import ContextManager

__all__ = [
    "ContextEntry",
    "LayerConfig",
    "ContextLayer",
    "MemoryManager",
    "RetrievalSystem",
    "SummarizationEngine",
    "ContextManager",
]

# Version of the context management package
__version__ = "1.0.0"
