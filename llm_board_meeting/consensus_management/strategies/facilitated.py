# llm_board_meeting/consensus_management/strategies/facilitated.py

"""
Facilitated consensus strategy for the LLM Board Meeting system.

This module implements a facilitated approach to consensus building that leverages
the Facilitator's expertise in managing group dynamics and resolving conflicts.
"""

from typing import Any, Dict, List, Optional, Sequence

from llm_board_meeting.consensus_management.strategies.base import ConsensusStrategy
from llm_board_meeting.consensus_management.models import ConsensusEntry
from llm_board_meeting.core.board_member import BoardMember


class FacilitatedStrategy(ConsensusStrategy):
    """Implements facilitated consensus building."""

    async def process(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, Any]:
        """Process consensus through facilitated discussion.

        Args:
            entry: The consensus entry to process.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing facilitated consensus results.
        """
        # Find the Facilitator among board members
        facilitator = next(
            (member for member in board_members if member.role == "Facilitator"), None
        )

        if not facilitator:
            return {
                "status": "failed",
                "reason": "No Facilitator available for facilitated consensus",
                "confidence": 0.0,
            }

        # Start with climate assessment
        climate_assessment = await self._assess_discussion_climate(
            facilitator, entry, board_members
        )

        if climate_assessment["safety_level"] < 0.6:
            # Address psychological safety concerns first
            await self._improve_discussion_climate(facilitator, climate_assessment)

        # Facilitate structured discussion
        discussion_results = await self._facilitate_discussion(
            facilitator, entry, board_members, climate_assessment
        )

        # Track participation and balance
        participation_stats = await self._track_participation(
            facilitator, discussion_results
        )

        # Evaluate consensus achievement
        consensus_achieved = self._evaluate_consensus(
            discussion_results, participation_stats
        )

        return {
            "status": "achieved" if consensus_achieved else "in_progress",
            "climate_assessment": climate_assessment,
            "discussion_results": discussion_results,
            "participation_stats": participation_stats,
            "rounds": len(discussion_results["rounds"]),
        }

    async def _assess_discussion_climate(
        self,
        facilitator: BoardMember,
        entry: ConsensusEntry,
        board_members: Sequence[BoardMember],
    ) -> Dict[str, Any]:
        """Assess the discussion climate.

        Args:
            facilitator: The Facilitator board member.
            entry: The consensus entry being discussed.
            board_members: All participating board members.

        Returns:
            Dict containing climate assessment.
        """
        # Get feedback from all members
        member_feedback = {}
        for member in board_members:
            if member != facilitator:
                feedback = await member.provide_feedback(
                    entry.content, "climate_assessment"
                )
                member_feedback[member.role] = feedback

        # Have facilitator assess the climate
        indicators = {
            "participation_balance": self._calculate_participation_balance(
                member_feedback
            ),
            "psychological_safety": self._assess_psychological_safety(member_feedback),
            "tension_level": self._assess_tension_level(member_feedback),
        }

        tension_points = [
            point
            for feedback in member_feedback.values()
            for point in feedback.get("tension_points", [])
        ]

        recommendations = [
            rec
            for feedback in member_feedback.values()
            for rec in feedback.get("recommendations", [])
        ]

        return {
            "indicators": indicators,
            "safety_level": indicators["psychological_safety"],
            "tension_points": tension_points,
            "recommendations": recommendations,
        }

    async def _improve_discussion_climate(
        self, facilitator: BoardMember, climate_assessment: Dict[str, Any]
    ) -> None:
        """Improve the discussion climate based on assessment.

        Args:
            facilitator: The Facilitator board member.
            climate_assessment: The current climate assessment.
        """
        for tension in climate_assessment["tension_points"]:
            await facilitator.record_intervention(
                topic=tension,
                situation="Low psychological safety",
                intervention_type="climate_improvement",
                approach="supportive_facilitation",
            )

    async def _facilitate_discussion(
        self,
        facilitator: BoardMember,
        entry: ConsensusEntry,
        board_members: Sequence[BoardMember],
        climate_assessment: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Facilitate the consensus discussion.

        Args:
            facilitator: The Facilitator board member.
            entry: The consensus entry being discussed.
            board_members: All participating board members.
            climate_assessment: The current climate assessment.

        Returns:
            Dict containing discussion results.
        """
        rounds = []
        max_rounds = self.config.max_discussion_rounds

        for round_num in range(max_rounds):
            # Get contributions from all members
            round_contributions = {}
            for member in board_members:
                if member != facilitator:
                    contribution = await member.contribute_to_discussion(
                        entry.topic,
                        {
                            "round": round_num,
                            "previous_rounds": rounds,
                            "climate": climate_assessment,
                        },
                    )
                    round_contributions[member.role] = contribution

            # Have facilitator analyze the round
            round_analysis = await facilitator.analyze_discussion(
                [contribution for contribution in round_contributions.values()]
            )

            # Record any necessary interventions
            if round_analysis.get("requires_intervention", False):
                await facilitator.record_intervention(
                    topic=entry.topic,
                    situation=round_analysis["situation"],
                    intervention_type=round_analysis["intervention_type"],
                    approach=round_analysis["approach"],
                )

            rounds.append(
                {
                    "round": round_num,
                    "contributions": round_contributions,
                    "analysis": round_analysis,
                }
            )

            # Check if consensus is emerging
            if self._evaluate_consensus({"rounds": rounds}, None):
                break

        return {"rounds": rounds}

    async def _track_participation(
        self, facilitator: BoardMember, discussion_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Track participation patterns in the discussion.

        Args:
            facilitator: The Facilitator board member.
            discussion_results: Results from the facilitated discussion.

        Returns:
            Dict containing participation statistics.
        """
        participation_counts = {}
        contribution_types = {}

        for round_data in discussion_results["rounds"]:
            for role, contribution in round_data["contributions"].items():
                participation_counts[role] = participation_counts.get(role, 0) + 1
                contribution_types[role] = contribution_types.get(role, [])
                contribution_types[role].append(contribution.get("type", "unknown"))

        return {
            "participation_counts": participation_counts,
            "contribution_types": contribution_types,
            "balance_metrics": self._calculate_participation_metrics(
                participation_counts
            ),
        }

    def _evaluate_consensus(
        self,
        discussion_results: Dict[str, Any],
        participation_stats: Optional[Dict[str, Any]],
    ) -> bool:
        """Evaluate if consensus has been reached.

        Args:
            discussion_results: Results from the facilitated discussion.
            participation_stats: Optional participation statistics.

        Returns:
            True if consensus achieved, False otherwise.
        """
        if not discussion_results["rounds"]:
            return False

        latest_round = discussion_results["rounds"][-1]

        # Check agreement levels from contributions
        agreement_scores = []
        for contribution in latest_round["contributions"].values():
            if "agreement_level" in contribution:
                agreement_scores.append(contribution["agreement_level"])

        if not agreement_scores:
            return False

        average_agreement = sum(agreement_scores) / len(agreement_scores)
        min_agreement = min(agreement_scores)

        # Consider both average and minimum agreement
        return (
            average_agreement >= self.config.discussion_agreement_threshold
            and min_agreement >= 0.6  # Ensure no strong objections
        )

    def _calculate_participation_balance(self, feedback: Dict[str, Any]) -> float:
        """Calculate participation balance from feedback.

        Args:
            feedback: Feedback from board members.

        Returns:
            Float between 0 and 1 indicating participation balance.
        """
        if not feedback:
            return 0.0

        participation_levels = [
            f.get("participation_level", 0.0) for f in feedback.values()
        ]

        if not participation_levels:
            return 0.0

        avg_participation = sum(participation_levels) / len(participation_levels)
        max_deviation = max(abs(p - avg_participation) for p in participation_levels)

        return 1.0 - (
            max_deviation / avg_participation if avg_participation > 0 else 1.0
        )

    def _assess_psychological_safety(self, feedback: Dict[str, Any]) -> float:
        """Assess psychological safety from feedback.

        Args:
            feedback: Feedback from board members.

        Returns:
            Float between 0 and 1 indicating psychological safety level.
        """
        if not feedback:
            return 0.0

        safety_indicators = [
            f.get("psychological_safety", 0.0) for f in feedback.values()
        ]

        return (
            sum(safety_indicators) / len(safety_indicators)
            if safety_indicators
            else 0.0
        )

    def _assess_tension_level(self, feedback: Dict[str, Any]) -> float:
        """Assess tension level from feedback.

        Args:
            feedback: Feedback from board members.

        Returns:
            Float between 0 and 1 indicating tension level.
        """
        if not feedback:
            return 0.0

        tension_indicators = [f.get("tension_level", 0.0) for f in feedback.values()]

        return (
            sum(tension_indicators) / len(tension_indicators)
            if tension_indicators
            else 0.0
        )

    def _calculate_participation_metrics(
        self, participation_counts: Dict[str, int]
    ) -> Dict[str, float]:
        """Calculate participation balance metrics.

        Args:
            participation_counts: Dict mapping roles to participation counts.

        Returns:
            Dict containing participation metrics.
        """
        if not participation_counts:
            return {"balance_score": 0.0, "engagement_score": 0.0}

        total_contributions = sum(participation_counts.values())
        expected_share = 1.0 / len(participation_counts)

        # Calculate deviation from equal participation
        participation_shares = {
            role: count / total_contributions
            for role, count in participation_counts.items()
        }

        max_deviation = max(
            abs(share - expected_share) for share in participation_shares.values()
        )

        return {
            "balance_score": 1.0 - (max_deviation / expected_share),
            "engagement_score": min(
                1.0, total_contributions / (len(participation_counts) * 3)
            ),
        }
