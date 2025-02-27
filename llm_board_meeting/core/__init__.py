# llm_board_meeting/core/__init__.py

"""
Core components of the LLM Board Meeting system.

This package contains the fundamental components and interfaces for the board
meeting system, including board member definitions, meeting management, and
consensus building.
"""

from llm_board_meeting.core.board_member import BoardMember
from llm_board_meeting.core.meeting import Meeting
from llm_board_meeting.core.consensus import ConsensusStrategy

__all__ = [
    "BoardMember",
    "Meeting",
    "ConsensusStrategy",
]
