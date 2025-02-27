# llm_board_meeting/meeting_formats/strategic_planning.py

"""
Strategic Planning meeting format for the LLM Board Meeting system.

This module implements a structured strategic planning format with phases for
environmental analysis, vision setting, strategy formulation, initiative
planning, and execution framework development.
"""

from typing import Dict, List, Any

from llm_board_meeting.meeting_formats.base_format import MeetingFormat


class StrategicPlanningFormat(MeetingFormat):
    """Implementation of a strategic planning format.

    Phases:
    1. Environmental Analysis: Assess internal and external factors
    2. Vision Setting: Define future state and objectives
    3. Strategy Formulation: Develop strategic approaches
    4. Initiative Planning: Define key initiatives
    5. Execution Framework: Plan implementation approach
    """

    def _get_default_time_allocation(self) -> Dict[str, int]:
        """Get default time allocation for strategic planning phases.

        Returns:
            Dict mapping phase names to time in minutes.
        """
        return {
            "environmental_analysis": 30,
            "vision_setting": 25,
            "strategy_formulation": 35,
            "initiative_planning": 25,
            "execution_framework": 25,
        }

    def get_phases(self) -> List[str]:
        """Get the ordered list of strategic planning phases.

        Returns:
            List of phase names in order.
        """
        return [
            "environmental_analysis",
            "vision_setting",
            "strategy_formulation",
            "initiative_planning",
            "execution_framework",
        ]

    def get_phase_prompt(self, phase: str, context: Dict[str, Any]) -> str:
        """Get the prompt template for a strategic planning phase.

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
            "environmental_analysis": """
                Let's analyze our internal and external environment.
                Consider:
                1. What are our strengths and weaknesses?
                2. What opportunities and threats exist?
                3. What market trends affect us?
                4. What are our key capabilities?

                Please share your environmental analysis.
                """,
            "vision_setting": """
                Let's define our vision and objectives.
                Consider:
                1. What is our desired future state?
                2. What are our key objectives?
                3. How do we measure success?
                4. What timeframe are we planning for?

                Please help articulate our vision and goals.
                """,
            "strategy_formulation": """
                Let's develop our strategic approach.
                Consider:
                1. What are our strategic options?
                2. How do we leverage our strengths?
                3. How do we address weaknesses?
                4. What competitive advantages can we build?

                Please propose strategic approaches.
                """,
            "initiative_planning": """
                Let's define our key initiatives.
                Consider:
                1. What major projects are needed?
                2. How do initiatives align with strategy?
                3. What resources are required?
                4. What are our priorities?

                Please propose key strategic initiatives.
                """,
            "execution_framework": """
                Let's plan our implementation approach.
                Consider:
                1. How will we organize for execution?
                2. What governance is needed?
                3. How will we track progress?
                4. How will we manage risks?

                Please help define our execution framework.
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
            "environmental_analysis": [
                "StrategicThinker",
                "Analyst",
                "Futurist",
                "DevilsAdvocate",
            ],
            "vision_setting": [
                "StrategicThinker",
                "Innovator",
                "EthicalOverseer",
                "Futurist",
            ],
            "strategy_formulation": [
                "StrategicThinker",
                "Synthesizer",
                "DevilsAdvocate",
                "Pragmatist",
            ],
            "initiative_planning": [
                "Pragmatist",
                "TechnicalExpert",
                "FinancialAnalyst",
                "StrategicThinker",
            ],
            "execution_framework": [
                "Pragmatist",
                "TechnicalExpert",
                "FinancialAnalyst",
                "DevilsAdvocate",
            ],
        }

        return base_roles + phase_roles[phase]

    def check_phase_completion(self, phase: str, context: Dict[str, Any]) -> bool:
        """Check if a strategic planning phase is complete.

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
            "environmental_analysis": self._check_environmental_analysis_completion,
            "vision_setting": self._check_vision_setting_completion,
            "strategy_formulation": self._check_strategy_formulation_completion,
            "initiative_planning": self._check_initiative_planning_completion,
            "execution_framework": self._check_execution_framework_completion,
        }

        return criteria[phase](context)

    def _check_environmental_analysis_completion(self, context: Dict[str, Any]) -> bool:
        """Check if environmental analysis phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        analysis = context.get("environmental_analysis", {})
        required_components = [
            "strengths",
            "weaknesses",
            "opportunities",
            "threats",
            "market_trends",
            "capabilities",
        ]
        return all(component in analysis for component in required_components) and all(
            len(analysis[component]) >= 2 for component in required_components
        )

    def _check_vision_setting_completion(self, context: Dict[str, Any]) -> bool:
        """Check if vision setting phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        vision = context.get("strategic_vision", {})
        required_components = [
            "vision_statement",
            "objectives",
            "success_metrics",
            "timeframe",
        ]
        return (
            all(component in vision for component in required_components)
            and len(vision["objectives"]) >= 3
            and all("metric" in obj and "target" in obj for obj in vision["objectives"])
        )

    def _check_strategy_formulation_completion(self, context: Dict[str, Any]) -> bool:
        """Check if strategy formulation phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        strategy = context.get("strategy", {})
        required_components = [
            "strategic_options",
            "selected_approach",
            "competitive_advantages",
            "risk_mitigation",
        ]
        return (
            all(component in strategy for component in required_components)
            and len(strategy["strategic_options"]) >= 2
            and all(
                all(k in opt for k in ["description", "rationale", "impact"])
                for opt in strategy["strategic_options"]
            )
        )

    def _check_initiative_planning_completion(self, context: Dict[str, Any]) -> bool:
        """Check if initiative planning phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        initiatives = context.get("strategic_initiatives", [])
        return len(initiatives) >= 3 and all(
            all(
                k in init
                for k in [
                    "name",
                    "description",
                    "alignment",
                    "resources",
                    "priority",
                ]
            )
            for init in initiatives
        )

    def _check_execution_framework_completion(self, context: Dict[str, Any]) -> bool:
        """Check if execution framework phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        framework = context.get("execution_framework", {})
        required_components = [
            "organization_structure",
            "governance_model",
            "progress_tracking",
            "risk_management",
            "resource_allocation",
        ]
        return all(component in framework for component in required_components)
