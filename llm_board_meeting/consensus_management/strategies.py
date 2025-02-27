# llm_board_meeting/consensus_management/strategies.py

"""
Implementations of different consensus strategies.

This module provides concrete implementations of various consensus building
approaches, following the Strategy Pattern from the base ConsensusStrategy.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence
import numpy as np
from scipy import stats

from llm_board_meeting.core.board_member import BoardMember
from llm_board_meeting.consensus_management.models import (
    ConsensusEntry,
    ConsensusConfig,
)


class BaseConsensusStrategy(ABC):
    """Abstract base class for consensus strategies."""

    def __init__(self, config: ConsensusConfig):
        """Initialize the strategy.

        Args:
            config: Configuration for the consensus mechanism.
        """
        self.config = config
        self.current_entry: Optional[ConsensusEntry] = None

    @abstractmethod
    async def build_consensus(
        self, board_members: List[BoardMember], entry: ConsensusEntry
    ) -> Dict[str, Any]:
        """Build consensus using this strategy.

        Args:
            board_members: List of participating board members.
            entry: The consensus entry to work with.

        Returns:
            Dict containing consensus results.
        """
        pass


class WeightedVotingStrategy(BaseConsensusStrategy):
    """Implementation of weighted voting consensus."""

    async def build_consensus(
        self, board_members: List[BoardMember], entry: ConsensusEntry
    ) -> Dict[str, Any]:
        """Build consensus through weighted voting.

        Args:
            board_members: List of participating board members.
            entry: The consensus entry to work with.

        Returns:
            Dict containing voting results.
        """
        total_supporting_weight = sum(entry.supporting_votes.values())
        total_opposing_weight = sum(entry.opposing_votes.values())
        total_weight = total_supporting_weight + total_opposing_weight

        if total_weight == 0:
            return {
                "status": "failed",
                "reason": "No votes recorded",
                "confidence": 0.0,
            }

        support_ratio = total_supporting_weight / total_weight
        confidence = support_ratio if support_ratio >= 0.5 else 1 - support_ratio

        return {
            "status": "achieved" if support_ratio > 0.5 else "rejected",
            "support_ratio": support_ratio,
            "confidence": confidence,
            "total_votes": len(entry.supporting_votes) + len(entry.opposing_votes),
            "timestamp": datetime.now().isoformat(),
        }


class DelphiMethodStrategy(BaseConsensusStrategy):
    """Implementation of Delphi method consensus."""

    async def build_consensus(
        self, board_members: List[BoardMember], entry: ConsensusEntry
    ) -> Dict[str, Any]:
        """Build consensus through Delphi method.

        Args:
            board_members: List of participating board members.
            entry: The consensus entry to work with.

        Returns:
            Dict containing Delphi results.
        """
        if entry.iteration_count >= self.config.max_iterations:
            # Analyze final convergence
            positions = [
                feedback["position_score"]
                for feedback in entry.feedback_history[-len(board_members) :]
            ]
            mean_position = np.mean(positions)
            std_position = np.std(positions)

            # Check for convergence
            convergence_achieved = std_position < 0.2  # Threshold for agreement

            return {
                "status": "achieved" if convergence_achieved else "rejected",
                "final_position": mean_position,
                "convergence_measure": 1 - std_position,  # Higher is more converged
                "confidence": 1 - std_position,
                "iterations_completed": entry.iteration_count,
                "timestamp": datetime.now().isoformat(),
            }

        return {
            "status": "in_progress",
            "current_iteration": entry.iteration_count,
            "remaining_iterations": self.config.max_iterations - entry.iteration_count,
            "timestamp": datetime.now().isoformat(),
        }


class BayesianAggregationStrategy(BaseConsensusStrategy):
    """Implementation of Bayesian aggregation consensus."""

    async def build_consensus(
        self, board_members: List[BoardMember], entry: ConsensusEntry
    ) -> Dict[str, Any]:
        """Build consensus through Bayesian aggregation.

        Args:
            board_members: List of participating board members.
            entry: The consensus entry to work with.

        Returns:
            Dict containing Bayesian results.
        """
        # Extract probabilities and weights from votes
        probabilities = []
        weights = []

        for role, weight in entry.supporting_votes.items():
            probabilities.append(1.0)  # Supporting votes indicate high probability
            weights.append(weight)

        for role, weight in entry.opposing_votes.items():
            probabilities.append(0.0)  # Opposing votes indicate low probability
            weights.append(weight)

        if not probabilities:
            return {
                "status": "failed",
                "reason": "No probabilistic evidence available",
                "confidence": 0.0,
            }

        # Calculate weighted average probability
        weighted_prob = np.average(probabilities, weights=weights)

        # Calculate confidence based on evidence strength
        evidence_strength = sum(weights)
        max_strength = len(board_members) * max(self.config.voting_weights.values())
        confidence = evidence_strength / max_strength

        return {
            "status": "achieved" if weighted_prob > 0.5 else "rejected",
            "probability": weighted_prob,
            "confidence": confidence,
            "evidence_strength": evidence_strength,
            "timestamp": datetime.now().isoformat(),
        }


class MetaAnalysisStrategy(BaseConsensusStrategy):
    """Implementation of meta-analysis (chair synthesis) consensus."""

    async def build_consensus(
        self, board_members: List[BoardMember], entry: ConsensusEntry
    ) -> Dict[str, Any]:
        """Build consensus through meta-analysis.

        Args:
            board_members: List of participating board members.
            entry: The consensus entry to work with.

        Returns:
            Dict containing meta-analysis results.
        """
        # Analyze feedback history for agreement patterns
        feedback_positions = [
            feedback.get("position_score", 0.5) for feedback in entry.feedback_history
        ]

        if not feedback_positions:
            return {
                "status": "failed",
                "reason": "No feedback available for meta-analysis",
                "confidence": 0.0,
            }

        # Calculate agreement metrics
        mean_position = np.mean(feedback_positions)
        agreement_strength = 1 - np.std(feedback_positions)

        # Analyze feedback themes
        themes = {}
        for feedback in entry.feedback_history:
            for theme in feedback.get("themes", []):
                themes[theme] = themes.get(theme, 0) + 1

        return {
            "status": "achieved" if agreement_strength > 0.7 else "in_progress",
            "agreement_strength": agreement_strength,
            "mean_position": mean_position,
            "common_themes": sorted(themes.items(), key=lambda x: x[1], reverse=True),
            "confidence": agreement_strength,
            "timestamp": datetime.now().isoformat(),
        }


class HybridStrategy(BaseConsensusStrategy):
    """Implementation of hybrid consensus approach."""

    async def build_consensus(
        self, board_members: List[BoardMember], entry: ConsensusEntry
    ) -> Dict[str, Any]:
        """Build consensus through hybrid approach.

        Args:
            board_members: List of participating board members.
            entry: The consensus entry to work with.

        Returns:
            Dict containing hybrid results.
        """
        # Apply different strategies based on entry characteristics
        results = {}

        # Use weighted voting for clear support/oppose patterns
        if entry.supporting_votes or entry.opposing_votes:
            voting_strategy = WeightedVotingStrategy(self.config)
            results["voting"] = await voting_strategy.build_consensus(
                board_members, entry
            )

        # Use Delphi for iterative feedback
        if entry.feedback_history:
            delphi_strategy = DelphiMethodStrategy(self.config)
            results["delphi"] = await delphi_strategy.build_consensus(
                board_members, entry
            )

        # Use meta-analysis for qualitative synthesis
        meta_strategy = MetaAnalysisStrategy(self.config)
        results["meta"] = await meta_strategy.build_consensus(board_members, entry)

        # Combine results
        confidence_scores = [
            r["confidence"] for r in results.values() if "confidence" in r
        ]

        if not confidence_scores:
            return {
                "status": "failed",
                "reason": "No strategy produced valid results",
                "confidence": 0.0,
            }

        # Calculate overall confidence and status
        overall_confidence = np.mean(confidence_scores)
        positive_results = sum(
            1 for r in results.values() if r.get("status") == "achieved"
        )

        return {
            "status": (
                "achieved" if positive_results > len(results) / 2 else "in_progress"
            ),
            "confidence": overall_confidence,
            "strategy_results": results,
            "timestamp": datetime.now().isoformat(),
        }
