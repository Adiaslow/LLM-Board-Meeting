# llm_board_meeting/meeting_formats/brainstorming.py

"""
Brainstorming meeting format for the LLM Board Meeting system.

This module implements a structured brainstorming session format with phases for
problem framing, idea generation, clustering, and evaluation.
"""

from typing import Dict, List, Any

from llm_board_meeting.meeting_formats.base_format import MeetingFormat


class BrainstormingFormat(MeetingFormat):
    """Implementation of a brainstorming session format.

    Phases:
    1. Problem Framing: Define scope and objectives
    2. Divergent Thinking: Unconstrained idea generation
    3. Idea Clustering: Organize concepts by theme
    4. Evaluation: Assess and prioritize ideas
    """

    def _get_default_time_allocation(self) -> Dict[str, int]:
        """Get default time allocation for brainstorming phases.

        Returns:
            Dict mapping phase names to time in minutes.
        """
        return {
            "problem_framing": 15,
            "divergent_thinking": 30,
            "idea_clustering": 20,
            "evaluation": 25,
        }

    def get_phases(self) -> List[str]:
        """Get the ordered list of brainstorming phases.

        Returns:
            List of phase names in order.
        """
        return [
            "problem_framing",
            "divergent_thinking",
            "idea_clustering",
            "evaluation",
        ]

    def get_phase_prompt(self, phase: str, context: Dict[str, Any]) -> str:
        """Get the prompt template for a brainstorming phase.

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
            "problem_framing": """
                As we begin this brainstorming session, let's clearly define our problem and objectives.
                Consider:
                1. What specific challenge are we addressing?
                2. What are our key constraints?
                3. What would success look like?
                4. What aspects should we focus on?

                Please share your perspective on these points.
                """,
            "divergent_thinking": """
                Now it's time for open ideation. Remember:
                - There are no bad ideas
                - Build on others' suggestions
                - Quantity over quality
                - Think beyond conventional solutions
                - Defer judgment

                What ideas do you have for addressing our challenge?
                """,
            "idea_clustering": """
                Let's organize the ideas we've generated into themes.
                Consider:
                1. What patterns do you see?
                2. How might these ideas be grouped?
                3. What relationships exist between different concepts?
                4. What key themes emerge?

                Please help categorize and connect these ideas.
                """,
            "evaluation": """
                It's time to evaluate our ideas. Consider:
                1. Alignment with objectives
                2. Feasibility of implementation
                3. Potential impact
                4. Resource requirements
                5. Risks and challenges

                Please assess the ideas based on these criteria.
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
            "problem_framing": [
                "TechnicalExpert",
                "StrategicThinker",
                "UserAdvocate",
            ],
            "divergent_thinking": [
                "Innovator",
                "DevilsAdvocate",
                "Futurist",
            ],
            "idea_clustering": [
                "Synthesizer",
                "StrategicThinker",
            ],
            "evaluation": [
                "Pragmatist",
                "TechnicalExpert",
                "FinancialAnalyst",
                "EthicalOverseer",
            ],
        }

        return base_roles + phase_roles[phase]

    def check_phase_completion(self, phase: str, context: Dict[str, Any]) -> bool:
        """Check if a brainstorming phase is complete.

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
            "problem_framing": self._check_problem_framing_completion,
            "divergent_thinking": self._check_divergent_thinking_completion,
            "idea_clustering": self._check_idea_clustering_completion,
            "evaluation": self._check_evaluation_completion,
        }

        return criteria[phase](context)

    def _check_problem_framing_completion(self, context: Dict[str, Any]) -> bool:
        """Check if problem framing phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        required_fields = [
            "problem_statement",
            "objectives",
            "constraints",
            "success_criteria",
        ]
        return all(field in context for field in required_fields)

    def _check_divergent_thinking_completion(self, context: Dict[str, Any]) -> bool:
        """Check if divergent thinking phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        ideas = context.get("generated_ideas", [])
        min_ideas = self.config.get("min_ideas", 10)
        return len(ideas) >= min_ideas

    def _check_idea_clustering_completion(self, context: Dict[str, Any]) -> bool:
        """Check if idea clustering phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        clusters = context.get("idea_clusters", {})
        unclustered = context.get("unclustered_ideas", [])
        return len(clusters) > 0 and len(unclustered) == 0

    def _check_evaluation_completion(self, context: Dict[str, Any]) -> bool:
        """Check if evaluation phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        evaluated_ideas = context.get("evaluated_ideas", {})
        total_ideas = len(context.get("generated_ideas", []))
        return len(evaluated_ideas) == total_ideas
