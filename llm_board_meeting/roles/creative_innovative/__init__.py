# llm_board_meeting/roles/creative_innovative/__init__.py

"""
Creative and innovative role implementations for the LLM Board Meeting system.

This package contains implementations of board members focused on innovation:
- Innovator: Generates novel concepts and makes unexpected connections
- Pragmatist: Focuses on practicality and implementation details
"""

from llm_board_meeting.roles.creative_innovative.innovator import Innovator
from llm_board_meeting.roles.creative_innovative.pragmatist import Pragmatist

__all__ = [
    "Innovator",
    "Pragmatist",
]
