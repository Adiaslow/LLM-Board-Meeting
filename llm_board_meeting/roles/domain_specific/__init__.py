# llm_board_meeting/roles/domain_specific/__init__.py

"""
Domain-specific role implementations for the LLM Board Meeting system.

This package contains implementations of board members with domain expertise:
- Technical Expert: Focuses on technical feasibility and implementation
- Strategic Thinker: Evaluates long-term implications and opportunities
- Financial Analyst: Assesses costs and resource requirements
- User Advocate: Represents end-user perspectives and needs
"""

from llm_board_meeting.roles.domain_specific.technical_expert import TechnicalExpert
from llm_board_meeting.roles.domain_specific.strategic_thinker import StrategicThinker
from llm_board_meeting.roles.domain_specific.financial_analyst import FinancialAnalyst
from llm_board_meeting.roles.domain_specific.user_advocate import UserAdvocate

__all__ = [
    "TechnicalExpert",
    "StrategicThinker",
    "FinancialAnalyst",
    "UserAdvocate",
]
