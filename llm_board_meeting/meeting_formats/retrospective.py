# llm_board_meeting/meeting_formats/retrospective.py

"""
Retrospective meeting format for the LLM Board Meeting system.

This module implements a structured retrospective format with phases for
data gathering, analysis, insight generation, action planning, and
learning documentation.
"""

from typing import Dict, List, Any

from llm_board_meeting.meeting_formats.base_format import MeetingFormat


class RetrospectiveFormat(MeetingFormat):
    """Implementation of a retrospective format.

    Phases:
    1. Data Gathering: Collect relevant metrics and feedback
    2. Analysis: Examine patterns and trends
    3. Insight Generation: Extract key learnings
    4. Action Planning: Define improvements
    5. Learning Documentation: Record insights for future use
    """

    def _get_default_time_allocation(self) -> Dict[str, int]:
        """Get default time allocation for retrospective phases.

        Returns:
            Dict mapping phase names to time in minutes.
        """
        return {
            "data_gathering": 25,
            "analysis": 30,
            "insight_generation": 25,
            "action_planning": 20,
            "learning_documentation": 20,
        }

    def get_phases(self) -> List[str]:
        """Get the ordered list of retrospective phases.

        Returns:
            List of phase names in order.
        """
        return [
            "data_gathering",
            "analysis",
            "insight_generation",
            "action_planning",
            "learning_documentation",
        ]

    def get_phase_prompt(self, phase: str, context: Dict[str, Any]) -> str:
        """Get the prompt template for a retrospective phase.

        Args:
            phase: The phase to get the prompt for.
            context: Current meeting context.

        Returns:
            Prompt template string for the phase.

        Raises:
            ValueError: If phase is not valid for this format.
        """
        if phase not in self.get_phases():
            raise ValueError(f"Invalid phase: {phase}")

        prompts = {
            "data_gathering": """
                Let's collect relevant data for our retrospective.
                Consider:
                1. What metrics are available?
                2. What feedback have we received?
                3. What observations can we share?
                4. What documentation should we review?

                Please share relevant data points and observations.
                """,
            "analysis": """
                Let's analyze the data we've gathered.
                Consider:
                1. What patterns do we see?
                2. How do different factors relate?
                3. What trends are emerging?
                4. What comparisons are meaningful?

                Please share your analysis of the data.
                """,
            "insight_generation": """
                Let's extract key insights from our analysis.
                Consider:
                1. What worked well and why?
                2. What could be improved and how?
                3. What surprised us?
                4. What did we learn?

                Please share your key insights and learnings.
                """,
            "action_planning": """
                Let's plan improvements based on our insights.
                Consider:
                1. What specific actions should we take?
                2. How do we prioritize these actions?
                3. Who should be responsible?
                4. When should changes be implemented?

                Please propose concrete improvement actions.
                """,
            "learning_documentation": """
                Let's document our learnings for future reference.
                Consider:
                1. What are the key takeaways?
                2. What best practices should we capture?
                3. What warnings or cautions apply?
                4. How should this inform future work?

                Please help document our learnings.
                """,
        }

        return prompts[phase].strip()

    def get_phase_roles(self, phase: str) -> List[str]:
        """Get the roles that should participate in each phase.

        Args:
            phase: The phase to get roles for.

        Returns:
            List of role names that should participate.

        Raises:
            ValueError: If phase is not valid for this format.
        """
        if phase not in self.get_phases():
            raise ValueError(f"Invalid phase: {phase}")

        # Base roles that participate in all phases
        base_roles = ["Chairperson", "Secretary"]

        phase_roles = {
            "data_gathering": [
                "Analyst",
                "TechnicalExpert",
                "UserAdvocate",
                "FinancialAnalyst",
            ],
            "analysis": [
                "Analyst",
                "DevilsAdvocate",
                "StrategicThinker",
                "Synthesizer",
            ],
            "insight_generation": [
                "Synthesizer",
                "StrategicThinker",
                "DevilsAdvocate",
                "Pragmatist",
            ],
            "action_planning": [
                "Pragmatist",
                "TechnicalExpert",
                "StrategicThinker",
                "UserAdvocate",
            ],
            "learning_documentation": [
                "Synthesizer",
                "TechnicalExpert",
                "EthicalOverseer",
                "StrategicThinker",
            ],
        }

        return base_roles + phase_roles[phase]

    def check_phase_completion(self, phase: str, context: Dict[str, Any]) -> bool:
        """Check if a retrospective phase is complete.

        Args:
            phase: The phase to check.
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.

        Raises:
            ValueError: If phase is not valid for this format.
        """
        if phase not in self.get_phases():
            raise ValueError(f"Invalid phase: {phase}")

        # Get phase-specific completion criteria
        criteria = {
            "data_gathering": self._check_data_gathering_completion,
            "analysis": self._check_analysis_completion,
            "insight_generation": self._check_insight_generation_completion,
            "action_planning": self._check_action_planning_completion,
            "learning_documentation": self._check_learning_documentation_completion,
        }

        return criteria[phase](context)

    def _check_data_gathering_completion(self, context: Dict[str, Any]) -> bool:
        """Check if data gathering phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        data = context.get("gathered_data", {})
        required_categories = [
            "metrics",
            "feedback",
            "observations",
            "documentation",
        ]
        return all(category in data for category in required_categories) and all(
            len(data[category]) > 0 for category in required_categories
        )

    def _check_analysis_completion(self, context: Dict[str, Any]) -> bool:
        """Check if analysis phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        analysis = context.get("data_analysis", {})
        required_components = [
            "patterns",
            "relationships",
            "trends",
            "comparisons",
        ]
        return all(component in analysis for component in required_components)

    def _check_insight_generation_completion(self, context: Dict[str, Any]) -> bool:
        """Check if insight generation phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        insights = context.get("generated_insights", {})
        required_categories = [
            "successes",
            "improvements",
            "surprises",
            "lessons",
        ]
        return (
            all(category in insights for category in required_categories)
            and len(insights.get("lessons", [])) >= 3
        )

    def _check_action_planning_completion(self, context: Dict[str, Any]) -> bool:
        """Check if action planning phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        actions = context.get("improvement_actions", [])
        return len(actions) >= 2 and all(
            all(k in a for k in ["description", "priority", "owner", "timeline"])
            for a in actions
        )

    def _check_learning_documentation_completion(self, context: Dict[str, Any]) -> bool:
        """Check if learning documentation phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        documentation = context.get("learning_documentation", {})
        required_sections = [
            "key_takeaways",
            "best_practices",
            "warnings",
            "future_implications",
        ]
        return all(section in documentation for section in required_sections)
