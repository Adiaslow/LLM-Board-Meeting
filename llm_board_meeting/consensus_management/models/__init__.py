# llm_board_meeting/consensus_management/models/__init__.py

"""
Models package for consensus management in the LLM Board Meeting system.

This package provides the data structures used in consensus management,
including configuration and entry models.
"""

from llm_board_meeting.consensus_management.models.config import ConsensusConfig
from llm_board_meeting.consensus_management.models.entry import ConsensusEntry

__all__ = [
    "ConsensusConfig",
    "ConsensusEntry",
]
