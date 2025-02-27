# llm_board_meeting/roles/__init__.py

"""
Role implementations for the LLM Board Meeting system.

This package provides different role types for board members, each designed for
specific responsibilities and perspectives in the meeting process:

1. Functional Roles:
   - Chairperson: Guides meeting flow and ensures productive discussion
   - Devil's Advocate: Challenges assumptions and prevents groupthink
   - Secretary: Documents decisions and manages context hierarchy
   - Synthesizer: Combines perspectives and builds toward consensus

2. Domain-Specific Roles:
   - Financial Analyst: Assesses costs, ROI, and resource requirements
   - Strategic Thinker: Focuses on long-term implications and opportunities
   - Technical Expert: Provides implementation and feasibility insights
   - User Advocate: Represents end-user perspectives and needs

3. Creative/Innovative Roles:
   - Innovator: Generates novel concepts and makes unexpected connections
   - Pragmatist: Focuses on practical implementation and reality checks
   - Synthesizer: Combines ideas into cohesive frameworks

4. Specialty Roles:
   - Ethical Overseer: Evaluates moral implications and ensures compliance
   - Facilitator: Manages group dynamics and ensures inclusive discussion
   - Futurist: Projects trends and identifies emerging opportunities
"""

from llm_board_meeting.roles.base_llm_member import BaseLLMMember

from llm_board_meeting.roles.functional import (
    Chairperson,
    Secretary,
    DevilsAdvocate,
    Synthesizer,
)

from llm_board_meeting.roles.domain_specific import (
    TechnicalExpert,
    StrategicThinker,
    FinancialAnalyst,
    UserAdvocate,
)

from llm_board_meeting.roles.creative_innovative import (
    Innovator,
    Pragmatist,
)

from llm_board_meeting.roles.specialty import (
    EthicalOverseer,
    Facilitator,
    Futurist,
)

__all__ = [
    # Base Class
    "BaseLLMMember",
    # Functional Roles
    "Chairperson",
    "Secretary",
    "DevilsAdvocate",
    "Synthesizer",
    # Domain-Specific Roles
    "TechnicalExpert",
    "StrategicThinker",
    "FinancialAnalyst",
    "UserAdvocate",
    # Creative/Innovative Roles
    "Innovator",
    "Pragmatist",
    # Specialty Roles
    "EthicalOverseer",
    "Facilitator",
    "Futurist",
]
