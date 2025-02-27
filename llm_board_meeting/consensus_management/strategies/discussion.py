# llm_board_meeting/consensus_management/strategies/discussion.py

"""
Discussion-based consensus strategy for the LLM Board Meeting system.

This module implements a structured discussion approach to consensus building.
"""

from typing import Any, Dict, List, Sequence

from llm_board_meeting.consensus_management.strategies.base import ConsensusStrategy
from llm_board_meeting.consensus_management.models import ConsensusEntry
from llm_board_meeting.core.board_member import BoardMember


class DiscussionBasedStrategy(ConsensusStrategy):
    """Implements discussion-based consensus building."""

    async def process(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> Dict[str, Any]:
        """Process consensus through structured discussion.

        Args:
            entry: The consensus entry to process.
            board_members: Sequence of board members participating in consensus.

        Returns:
            Dict containing discussion results and consensus status.
        """
        discussion_rounds = await self._facilitate_discussion(entry, board_members)
        consensus_achieved = self._evaluate_consensus(discussion_rounds)

        return {
            "status": "achieved" if consensus_achieved else "in_progress",
            "discussion_rounds": discussion_rounds,
            "rounds": len(discussion_rounds),
        }

    async def _facilitate_discussion(
        self, entry: ConsensusEntry, board_members: Sequence[BoardMember]
    ) -> List[Dict[str, Any]]:
        """Facilitate structured discussion rounds.

        Args:
            entry: The consensus entry to discuss.
            board_members: Sequence of board members participating in discussion.

        Returns:
            List of discussion round results.
        """
        discussion_rounds = []
        max_rounds = self.config.max_discussion_rounds

        for round_num in range(max_rounds):
            round_feedback = {}
            for member in board_members:
                feedback = await member.provide_feedback(
                    entry.content,
                    {
                        "round": round_num,
                        "previous_rounds": discussion_rounds,
                        "criteria": entry.metadata.get("criteria", {}),
                    },
                )
                round_feedback[member.role] = feedback

            discussion_rounds.append(
                {
                    "round": round_num,
                    "feedback": round_feedback,
                    "summary": self._summarize_round(round_feedback),
                }
            )

            if self._evaluate_consensus(discussion_rounds):
                break

        return discussion_rounds

    def _evaluate_consensus(self, discussion_rounds: List[Dict[str, Any]]) -> bool:
        """Evaluate if consensus has been reached through discussion.

        Args:
            discussion_rounds: List of discussion round results.

        Returns:
            True if consensus achieved, False otherwise.
        """
        if not discussion_rounds:
            return False

        latest_round = discussion_rounds[-1]
        agreement_threshold = self.config.discussion_agreement_threshold

        # Calculate agreement level from feedback
        feedback_values = [
            feedback.get("agreement", 0.0)
            for feedback in latest_round["feedback"].values()
        ]

        if not feedback_values:
            return False

        average_agreement = sum(feedback_values) / len(feedback_values)
        return average_agreement >= agreement_threshold

    def _summarize_round(self, round_feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize the results of a discussion round.

        Args:
            round_feedback: Feedback from all members for the round.

        Returns:
            Dict containing round summary.
        """
        agreements = []
        concerns = []
        suggestions = []

        for role, feedback in round_feedback.items():
            if feedback.get("agreement", 0.0) >= 0.8:
                agreements.extend(feedback.get("points", []))
            if feedback.get("agreement", 0.0) <= 0.4:
                concerns.extend(feedback.get("concerns", []))
            suggestions.extend(feedback.get("suggestions", []))

        return {
            "key_agreements": agreements,
            "main_concerns": concerns,
            "suggestions": suggestions,
            "total_feedback": len(round_feedback),
        }
