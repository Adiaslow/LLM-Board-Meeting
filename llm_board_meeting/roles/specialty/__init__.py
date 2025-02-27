# llm_board/roles/specialty/__init__.py

"""
Specialty role implementations for the LLM Board Meeting system.

This package contains implementations of board members with specialized focus:
- Ethical Overseer: Evaluates moral implications and identifies biases
- Futurist: Projects long-term trends and potential disruptions
- Facilitator: Resolves conflicts and ensures productive discourse
"""

from .ethical_overseer import EthicalOverseer
from .futurist import Futurist
from .facilitator import Facilitator

__all__ = [
    "EthicalOverseer",
    "Futurist",
    "Facilitator",
]
