# llm_board_meeting/meeting_formats/decision_analysis.py

"""
Decision Analysis meeting format for the LLM Board Meeting system.

This module implements a structured decision analysis format with phases for
options enumeration, criteria definition, systematic assessment, sensitivity
analysis, and final recommendation.
"""

from typing import Dict, List, Any

from llm_board_meeting.meeting_formats.base_format import MeetingFormat


class DecisionAnalysisFormat(MeetingFormat):
    """Implementation of a decision analysis format.

    Phases:
    1. Options Enumeration: List and detail potential options
    2. Criteria Definition: Define and weight evaluation criteria
    3. Systematic Assessment: Evaluate each option against criteria
    4. Sensitivity Analysis: Test robustness of conclusions
    5. Final Recommendation: Synthesize analysis into decision
    """

    def _get_default_time_allocation(self) -> Dict[str, int]:
        """Get default time allocation for decision analysis phases.

        Returns:
            Dict mapping phase names to time in minutes.
        """
        return {
            "options_enumeration": 20,
            "criteria_definition": 25,
            "systematic_assessment": 35,
            "sensitivity_analysis": 20,
            "final_recommendation": 20,
        }

    def get_phases(self) -> List[str]:
        """Get the ordered list of decision analysis phases.

        Returns:
            List of phase names in order.
        """
        return [
            "options_enumeration",
            "criteria_definition",
            "systematic_assessment",
            "sensitivity_analysis",
            "final_recommendation",
        ]

    def get_phase_prompt(self, phase: str, context: Dict[str, Any]) -> str:
        """Get the prompt template for a decision analysis phase.

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
            "options_enumeration": """
                Let's identify all potential options for our decision.
                Consider:
                1. What are all possible approaches?
                2. Are there hybrid or innovative alternatives?
                3. What are the key characteristics of each option?
                4. What assumptions underlie each option?

                Please share potential options and their details.
                """,
            "criteria_definition": """
                We need to define our evaluation criteria.
                Consider:
                1. What are our key decision criteria?
                2. How should we weight different factors?
                3. What are our must-have vs. nice-to-have criteria?
                4. How will we measure success for each criterion?

                Please propose criteria and their relative importance.
                """,
            "systematic_assessment": """
                Let's evaluate each option against our criteria.
                For each option, consider:
                1. Quantitative scores for each criterion
                2. Supporting evidence and rationale
                3. Risks and uncertainties
                4. Implementation considerations

                Please provide your assessment with clear justification.
                """,
            "sensitivity_analysis": """
                We'll test the robustness of our analysis.
                Consider:
                1. How do results change with different weights?
                2. What if our assumptions are wrong?
                3. What are the key uncertainties?
                4. Under what conditions might rankings change?

                Please analyze sensitivity to key factors.
                """,
            "final_recommendation": """
                Let's synthesize our analysis into a recommendation.
                Consider:
                1. Which option best meets our criteria?
                2. What are the key tradeoffs?
                3. What risks need to be managed?
                4. What are the next steps?

                Please provide your final recommendation with rationale.
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
            "options_enumeration": [
                "StrategicThinker",
                "Innovator",
                "TechnicalExpert",
                "UserAdvocate",
            ],
            "criteria_definition": [
                "StrategicThinker",
                "FinancialAnalyst",
                "EthicalOverseer",
                "Pragmatist",
            ],
            "systematic_assessment": [
                "Analyst",
                "TechnicalExpert",
                "FinancialAnalyst",
                "DevilsAdvocate",
            ],
            "sensitivity_analysis": [
                "Analyst",
                "DevilsAdvocate",
                "Pragmatist",
                "StrategicThinker",
            ],
            "final_recommendation": [
                "Synthesizer",
                "StrategicThinker",
                "EthicalOverseer",
                "Pragmatist",
            ],
        }

        return base_roles + phase_roles[phase]

    def check_phase_completion(self, phase: str, context: Dict[str, Any]) -> bool:
        """Check if a decision analysis phase is complete.

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
            "options_enumeration": self._check_options_enumeration_completion,
            "criteria_definition": self._check_criteria_definition_completion,
            "systematic_assessment": self._check_systematic_assessment_completion,
            "sensitivity_analysis": self._check_sensitivity_analysis_completion,
            "final_recommendation": self._check_final_recommendation_completion,
        }

        return criteria[phase](context)

    def _check_options_enumeration_completion(self, context: Dict[str, Any]) -> bool:
        """Check if options enumeration phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        options = context.get("decision_options", [])
        min_options = self.config.get("min_options", 3)
        return len(options) >= min_options and all(
            "description" in opt and "assumptions" in opt for opt in options
        )

    def _check_criteria_definition_completion(self, context: Dict[str, Any]) -> bool:
        """Check if criteria definition phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        criteria = context.get("evaluation_criteria", {})
        return (
            len(criteria) >= 3
            and all("weight" in c and "measure" in c for c in criteria.values())
            and sum(c["weight"] for c in criteria.values()) == 1.0
        )

    def _check_systematic_assessment_completion(self, context: Dict[str, Any]) -> bool:
        """Check if systematic assessment phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        assessments = context.get("option_assessments", {})
        options = context.get("decision_options", [])
        criteria = context.get("evaluation_criteria", {})

        return len(assessments) == len(options) and all(
            all(c in opt for c in criteria) for opt in assessments.values()
        )

    def _check_sensitivity_analysis_completion(self, context: Dict[str, Any]) -> bool:
        """Check if sensitivity analysis phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        sensitivity = context.get("sensitivity_analysis", {})
        required_analyses = [
            "weight_sensitivity",
            "assumption_impact",
            "uncertainty_ranges",
        ]
        return all(analysis in sensitivity for analysis in required_analyses)

    def _check_final_recommendation_completion(self, context: Dict[str, Any]) -> bool:
        """Check if final recommendation phase is complete.

        Args:
            context: Current meeting context.

        Returns:
            True if phase is complete, False otherwise.
        """
        recommendation = context.get("final_recommendation", {})
        required_fields = [
            "selected_option",
            "rationale",
            "tradeoffs",
            "risks",
            "next_steps",
        ]
        return all(field in recommendation for field in required_fields)
