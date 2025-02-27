# llm_board_meeting/roles/functional/__init__.py

"""
Functional role implementations for the LLM Board Meeting system.

This package contains implementations of board members with functional roles:
- Chairperson: Guides meeting flow and ensures participation
- Secretary: Documents key points and manages context
- Devil's Advocate: Challenges assumptions and prevents groupthink
- Synthesizer: Combines perspectives and builds consensus
"""

from llm_board_meeting.roles.functional.chairperson import Chairperson
from llm_board_meeting.roles.functional.secretary import Secretary
from llm_board_meeting.roles.functional.devils_advocate import DevilsAdvocate
from llm_board_meeting.roles.functional.synthesizer import Synthesizer

__all__ = [
    "Chairperson",
    "Secretary",
    "DevilsAdvocate",
    "Synthesizer",
]
