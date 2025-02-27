# llm_board_meeting/roles/functional/chairperson.py

"""
Chairperson implementation for the LLM Board Meeting system.

This module implements the Chairperson role, responsible for guiding meetings,
ensuring participation, and maintaining productive discourse.
"""

from typing import Any, Dict, List
import json
from datetime import datetime

from llm_board_meeting.roles.base_llm_member import BaseLLMMember


class Chairperson(BaseLLMMember):
    """Chairperson board member implementation.

    The Chairperson is responsible for:
    - Guiding the meeting flow
    - Ensuring all members contribute
    - Summarizing discussions
    - Managing time allocation
    - Maintaining focus on objectives
    """

    def __init__(
        self,
        name: str,
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        llm_config: Dict[str, Any],
    ) -> None:
        """Initialize a new Chairperson.

        Args:
            name: The name of the board member.
            expertise_areas: List of expertise areas.
            personality_profile: Dict containing personality configuration.
            llm_config: Configuration for the LLM (temperature, etc.).
        """
        super().__init__(
            name=name,
            role="Chairperson",
            expertise_areas=expertise_areas,
            personality_profile=personality_profile,
            system_prompt=self._get_base_system_prompt(),
            temperature=llm_config.get("temperature", 0.7),
            max_tokens=llm_config.get("max_tokens", 1000),
        )
        self.participation_stats: Dict[str, int] = {}
        self.time_allocations: Dict[str, float] = {}

    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for the Chairperson role.

        Returns:
            String containing the base system prompt.
        """
        return """You are serving as the Chairperson in a board meeting. Your role is to:
1. Guide the meeting flow and ensure it stays on track
2. Encourage participation from all board members
3. Maintain a balanced discussion
4. Summarize key points and decisions
5. Manage time effectively
6. Resolve conflicts and maintain productive discourse

Your communication style should be:
- Clear and authoritative but not domineering
- Inclusive and encouraging
- Focused on objectives
- Professional and diplomatic

When responding to discussions:
1. Acknowledge contributions
2. Guide the conversation toward objectives
3. Ensure all relevant perspectives are considered
4. Maintain meeting structure and timing
5. Summarize and clarify when needed"""

    def _get_role_specific_prompt(self) -> str:
        """Get Chairperson-specific prompt modifications.

        Returns:
            String containing role-specific prompt additions.
        """
        participation_summary = self._get_participation_summary()
        time_summary = self._get_time_summary()

        return f"""Current Meeting State:
- Participation Balance: {participation_summary}
- Time Allocation: {time_summary}

Remember to:
1. Address any participation imbalances
2. Maintain time constraints
3. Keep discussion focused on objectives"""

    def _get_evaluation_prompt(self) -> str:
        """Get the evaluation-specific system prompt.

        Returns:
            String containing the system prompt for evaluations.
        """
        return """As the Chairperson, evaluate this proposal considering:
1. Alignment with meeting objectives
2. Clarity and completeness
3. Feasibility of implementation
4. Impact on stakeholders
5. Resource requirements

Provide balanced, objective scoring that considers all perspectives."""

    def _get_feedback_prompt(self) -> str:
        """Get the feedback-specific system prompt.

        Returns:
            String containing the system prompt for feedback.
        """
        return """As the Chairperson, provide constructive feedback that:
1. Acknowledges positive aspects
2. Identifies areas for improvement
3. Suggests specific enhancements
4. Considers multiple perspectives
5. Maintains meeting productivity

Focus on actionable recommendations while maintaining group cohesion."""

    async def _generate_llm_response(
        self, system_prompt: str, context: Dict[str, Any], prompt: str, **kwargs
    ) -> Dict[str, Any]:
        """Generate a response using the LLM.

        Args:
            system_prompt: The system prompt for the LLM.
            context: The formatted context.
            prompt: The user prompt.
            **kwargs: Additional arguments for the LLM.

        Returns:
            Dict containing the LLM response and metadata.
        """
        # This is a placeholder - actual implementation would integrate with an LLM
        # For now, we'll return a mock response
        return {
            "content": "This is a placeholder response. Implement actual LLM integration.",
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.8,
            "metadata": {
                "role": "Chairperson",
                "context_tokens": len(str(context)),
                "prompt_tokens": len(prompt),
            },
        }

    def update_participation_stats(self, member_name: str) -> None:
        """Update participation statistics for a board member.

        Args:
            member_name: The name of the member who participated.
        """
        self.participation_stats[member_name] = (
            self.participation_stats.get(member_name, 0) + 1
        )

    def update_time_allocation(self, topic: str, duration: float) -> None:
        """Update time allocation statistics for a topic.

        Args:
            topic: The topic being discussed.
            duration: Time spent on the topic in minutes.
        """
        self.time_allocations[topic] = self.time_allocations.get(topic, 0.0) + duration

    def _get_participation_summary(self) -> str:
        """Get a summary of current participation statistics.

        Returns:
            String containing participation summary.
        """
        if not self.participation_stats:
            return "No participation data available"

        total = sum(self.participation_stats.values())
        summary = []
        for member, count in self.participation_stats.items():
            percentage = (count / total) * 100
            summary.append(f"{member}: {percentage:.1f}%")

        return ", ".join(summary)

    def _get_time_summary(self) -> str:
        """Get a summary of time allocations.

        Returns:
            String containing time allocation summary.
        """
        if not self.time_allocations:
            return "No time allocation data available"

        total = sum(self.time_allocations.values())
        summary = []
        for topic, duration in self.time_allocations.items():
            percentage = (duration / total) * 100
            summary.append(f"{topic}: {percentage:.1f}%")

        return ", ".join(summary)

    def _format_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format the context for Chairperson-specific needs.

        Args:
            context: Raw context dictionary.

        Returns:
            Formatted context dictionary.
        """
        base_context = super()._format_context(context)

        # Add Chairperson-specific context
        return {
            **base_context,
            "participation_stats": self.participation_stats,
            "time_allocations": self.time_allocations,
            "meeting_phase": context.get("meeting_phase", "unknown"),
            "remaining_time": context.get("remaining_time", "unknown"),
            "pending_topics": context.get("pending_topics", []),
        }
