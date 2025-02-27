# llm_board_meeting/roles/functional/devils_advocate.py

"""
Devil's Advocate implementation for the LLM Board Meeting system.

This module implements the Devil's Advocate role, responsible for critical analysis,
risk identification, and preventing groupthink through constructive challenges.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from llm_board_meeting.roles.base_llm_member import BaseLLMMember


class DevilsAdvocate(BaseLLMMember):
    """Devil's Advocate board member implementation.

    The Devil's Advocate is responsible for:
    - Challenging assumptions and conventional thinking
    - Identifying potential risks and weaknesses
    - Preventing groupthink through critical analysis
    - Strengthening proposals through constructive criticism
    - Surfacing hidden problems and edge cases
    """

    def __init__(
        self,
        name: str,
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        llm_config: Dict[str, Any],
        critical_focus_areas: List[str],
        risk_tolerance: str,
    ) -> None:
        """Initialize a new Devil's Advocate.

        Args:
            name: The name of the board member.
            expertise_areas: List of expertise areas.
            personality_profile: Dict containing personality configuration.
            llm_config: Configuration for the LLM (temperature, etc.).
            critical_focus_areas: Areas to focus critical analysis on.
            risk_tolerance: Level of risk tolerance for analysis.
        """
        # Initialize role-specific context
        role_specific_context = {
            "critical_focus_areas": critical_focus_areas,
            "risk_tolerance": risk_tolerance,
            "challenged_points": [],
            "identified_risks": [],
            "analysis_metrics": {
                "total_challenges": 0,
                "risks_identified": 0,
                "mitigations_proposed": 0,
            },
        }

        # Initialize base class with role-specific configuration
        super().__init__(
            name=name,
            role="DevilsAdvocate",
            expertise_areas=expertise_areas,
            personality_profile=personality_profile,
            role_specific_context=role_specific_context,
            llm_config=llm_config,
        )

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
        return {
            "content": "This is a placeholder response. Implement actual LLM integration.",
            "timestamp": datetime.now().isoformat(),
            "confidence": 0.85,
            "metadata": {
                "role": "Devil's Advocate",
                "context_tokens": len(str(context)),
                "prompt_tokens": len(prompt),
                "focus_areas": self.role_specific_context["critical_focus_areas"],
            },
        }

    def record_challenge(
        self, topic: str, assumption: str, challenge: str, evidence: List[str]
    ) -> None:
        """Record a challenge to an assumption.

        Args:
            topic: The topic being discussed.
            assumption: The assumption being challenged.
            challenge: The specific challenge raised.
            evidence: Supporting evidence for the challenge.
        """
        challenge_entry = {
            "topic": topic,
            "assumption": assumption,
            "challenge": challenge,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat(),
            "status": "open",
        }

        self.role_specific_context["challenged_points"].append(challenge_entry)
        self.role_specific_context["analysis_metrics"]["total_challenges"] += 1

    def identify_risk(
        self,
        topic: str,
        risk_type: str,
        description: str,
        severity: float,
        mitigation: Optional[str] = None,
    ) -> None:
        """Record an identified risk.

        Args:
            topic: The topic the risk relates to.
            risk_type: Category of risk identified.
            description: Detailed description of the risk.
            severity: Risk severity score (0-10).
            mitigation: Optional proposed mitigation strategy.
        """
        risk_entry = {
            "topic": topic,
            "type": risk_type,
            "description": description,
            "severity": severity,
            "mitigation": mitigation,
            "timestamp": datetime.now().isoformat(),
            "status": "active",
        }

        self.role_specific_context["identified_risks"].append(risk_entry)
        self.role_specific_context["analysis_metrics"]["risks_identified"] += 1
        if mitigation:
            self.role_specific_context["analysis_metrics"]["mitigations_proposed"] += 1

    def get_critical_analysis_summary(self) -> Dict[str, Any]:
        """Get a summary of critical analysis activities.

        Returns:
            Dict containing analysis summary.
        """
        return {
            "total_challenges": self.role_specific_context["analysis_metrics"][
                "total_challenges"
            ],
            "active_risks": [
                risk
                for risk in self.role_specific_context["identified_risks"]
                if risk["status"] == "active"
            ],
            "recent_challenges": self.role_specific_context["challenged_points"][-5:],
            "metrics": self.role_specific_context["analysis_metrics"],
        }

    def update_risk_status(
        self, risk_index: int, new_status: str, resolution_notes: Optional[str] = None
    ) -> None:
        """Update the status of an identified risk.

        Args:
            risk_index: Index of the risk in the identified_risks list.
            new_status: New status of the risk.
            resolution_notes: Optional notes about risk resolution.
        """
        if 0 <= risk_index < len(self.role_specific_context["identified_risks"]):
            risk = self.role_specific_context["identified_risks"][risk_index]
            risk["status"] = new_status
            if resolution_notes:
                risk["resolution_notes"] = resolution_notes
