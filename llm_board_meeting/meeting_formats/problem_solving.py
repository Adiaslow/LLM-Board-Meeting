# llm_board_meeting/meeting_formats/problem_solving.py

"""
Problem Solving meeting format for the LLM Board Meeting system.

This module implements a structured problem solving format with phases for
problem definition, root cause analysis, solution generation, implementation
planning, and monitoring setup.
"""

from typing import Dict, List, Any

from llm_board_meeting.meeting_formats.base_format import MeetingFormat


class ProblemSolvingFormat(MeetingFormat):
    """Implementation of a problem solving format.

    Phases:
    1. Problem Definition: Clear articulation of the issue
    2. Root Cause Analysis: Identify underlying causes
    3. Solution Generation: Develop potential solutions
    4. Implementation Planning: Detail execution steps
    5. Monitoring Setup: Define success metrics
    """

    def _get_default_time_allocation(self) -> Dict[str, int]:
        """Get default time allocation for problem solving phases.

        Returns:
            Dict mapping phase names to time in minutes.
        """
        return {
            "problem_definition": 20,
            "root_cause_analysis": 30,
            "solution_generation": 25,
            "implementation_planning": 25,
            "monitoring_setup": 20,
        }

    def get_phases(self) -> List[str]:
        """Get the ordered list of problem solving phases.

        Returns:
            List of phase names in order.
        """
        return [
            "problem_definition",
            "root_cause_analysis",
            "solution_generation",
            "implementation_planning",
            "monitoring_setup",
        ]

    def get_phase_prompt(self, phase: str, context: Dict[str, Any]) -> str:
        """Get the prompt template for a problem solving phase.

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
            "problem_definition": """
                Let's clearly define the problem we're addressing.
                Consider:
                1. What are the symptoms we're observing?
                2. Who is affected by this problem?
                3. What is the impact and scope?
                4. What are the boundaries of this problem?

                Please help articulate the problem statement.
                """,
            "root_cause_analysis": """
                Let's identify the root causes of our problem.
                Consider:
                1. Why does this problem occur?
                2. What are the contributing factors?
                3. How do these factors interact?
                4. Which causes are within our control?

                Please share your analysis of potential root causes.
                """,
            "solution_generation": """
                Let's develop potential solutions to address root causes.
                Consider:
                1. What solutions address each root cause?
                2. Are there preventive measures?
                3. What are short-term vs. long-term solutions?
                4. How might solutions be combined?

                Please propose potential solutions.
                """,
            "implementation_planning": """
                Let's plan the implementation of our solutions.
                Consider:
                1. What are the key action steps?
                2. What resources are needed?
                3. Who needs to be involved?
                4. What are potential obstacles?

                Please help develop the implementation plan.
                """,
            "monitoring_setup": """
                Let's define how we'll monitor success.
                Consider:
                1. What metrics indicate success?
                2. How will we track progress?
                3. What are our review points?
                4. When should we adjust the plan?

                Please propose monitoring mechanisms.
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
            "problem_definition": [
                "TechnicalExpert",
                "UserAdvocate",
                "DevilsAdvocate",
                "Synthesizer",
            ],
            "root_cause_analysis": [
                "TechnicalExpert",
                "Analyst",
                "DevilsAdvocate",
                "StrategicThinker",
            ],
            "solution_generation": [
                "Innovator",
                "TechnicalExpert",
                "Pragmatist",
                "StrategicThinker",
            ],
            "implementation_planning": [
                "Pragmatist",
                "TechnicalExpert",
                "FinancialAnalyst",
                "UserAdvocate",
            ],
            "monitoring_setup": [
                "Analyst",
                "TechnicalExpert",
                "Pragmatist",
                "DevilsAdvocate",
            ],
        }

        return base_roles + phase_roles[phase]

    def check_phase_completion(self, phase: str, context: Dict[str, Any]) -> bool:
        """Check if a problem solving phase is complete.

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
            "problem_definition": self._check_problem_definition_completion,
            "root_cause_analysis": self._check_root_cause_analysis_completion,
            "solution_generation": self._check_solution_generation_completion,
            "implementation_planning": self._check_implementation_planning_completion,
            "monitoring_setup": self._check_monitoring_setup_completion,
        }

        return criteria[phase](context)

    def _check_problem_definition_completion(self, context: Dict[str, Any]) -> bool:
        """Check if problem definition phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        problem = context.get("problem_statement", {})
        required_fields = [
            "description",
            "symptoms",
            "affected_parties",
            "impact",
            "scope",
        ]
        return all(field in problem for field in required_fields)

    def _check_root_cause_analysis_completion(self, context: Dict[str, Any]) -> bool:
        """Check if root cause analysis phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        analysis = context.get("root_cause_analysis", {})
        return (
            len(analysis.get("causes", [])) >= 2
            and len(analysis.get("contributing_factors", [])) >= 2
            and "cause_relationships" in analysis
        )

    def _check_solution_generation_completion(self, context: Dict[str, Any]) -> bool:
        """Check if solution generation phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        solutions = context.get("proposed_solutions", [])
        min_solutions = self.config.get("min_solutions", 3)
        return len(solutions) >= min_solutions and all(
            all(k in s for k in ["description", "addresses", "timeline", "resources"])
            for s in solutions
        )

    def _check_implementation_planning_completion(
        self, context: Dict[str, Any]
    ) -> bool:
        """Check if implementation planning phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        plan = context.get("implementation_plan", {})
        required_components = [
            "action_steps",
            "resource_requirements",
            "responsibilities",
            "timeline",
            "risk_mitigation",
        ]
        return all(component in plan for component in required_components)

    def _check_monitoring_setup_completion(self, context: Dict[str, Any]) -> bool:
        """Check if monitoring setup phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        monitoring = context.get("monitoring_plan", {})
        required_components = [
            "success_metrics",
            "tracking_methods",
            "review_schedule",
            "adjustment_criteria",
        ]
        return all(component in monitoring for component in required_components)
