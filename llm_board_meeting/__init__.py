# llm_board_meeting/__init__.py

"""
LLM Board Meeting System

A framework for simulating board meetings using multiple LLMs with different roles
and perspectives, featuring context management, meeting formats, and consensus building.
"""

from llm_board_meeting.core.board_member import BoardMember
from llm_board_meeting.core.meeting import Meeting
from llm_board_meeting.consensus_management.manager import ConsensusManager
from llm_board_meeting.context_management.manager import ContextManager
from llm_board_meeting.roles.base_llm_member import BaseLLMMember

__version__ = "1.0.0"

__all__ = [
    "BoardMember",
    "BaseLLMMember",
    "Meeting",
    "ConsensusManager",
    "ContextManager",
]
