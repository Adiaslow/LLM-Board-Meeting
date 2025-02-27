# llm_board_meeting/consensus_management/models/config.py

"""
Configuration model for consensus management in the LLM Board Meeting system.

This module defines the configuration data structure used for managing consensus
building processes, including voting weights, thresholds, and timing parameters.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class ConsensusConfig:
    """Configuration for consensus management.

    Attributes:
        voting_weights: Dictionary mapping roles to their voting weight multipliers.
        max_discussion_rounds: Maximum number of discussion rounds before forcing decision.
        discussion_agreement_threshold: Minimum agreement level to consider consensus reached.
        min_participants: Minimum number of participants required for valid consensus.
        timeout_minutes: Maximum time allowed for consensus building.
    """

    voting_weights: Dict[str, float] = field(
        default_factory=lambda: {
            "Chairperson": 1.2,
            "Secretary": 1.0,
            "DevilsAdvocate": 1.1,
            "Synthesizer": 1.0,
            "TechnicalExpert": 1.1,
            "StrategicThinker": 1.1,
            "FinancialAnalyst": 1.1,
            "UserAdvocate": 1.0,
            "Innovator": 0.9,
            "Pragmatist": 1.0,
            "EthicalOverseer": 1.1,
            "Facilitator": 1.0,
            "Futurist": 0.9,
        }
    )
    max_discussion_rounds: int = 5
    discussion_agreement_threshold: float = 0.75
    min_participants: int = 3
    timeout_minutes: int = 30
