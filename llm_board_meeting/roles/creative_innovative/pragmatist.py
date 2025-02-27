# llm_board_meeting/roles/functional/pragmatist.py

"""
Pragmatist implementation for the LLM Board Meeting system.

This module implements the Pragmatist role, responsible for practical
implementation considerations, feasibility assessment, and actionable planning.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from llm_board_meeting.roles.base_llm_member import BaseLLMMember


class Pragmatist(BaseLLMMember):
    """Pragmatist board member implementation.

    The Pragmatist is responsible for:
    - Focusing on practical implementation
    - Considering real-world constraints
    - Breaking down ideas into actionable steps
    - Ensuring feasibility of proposals
    - Maintaining operational perspective
    """

    def __init__(
        self,
        name: str,
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        llm_config: Dict[str, Any],
        implementation_focus: str,
        resource_context: Dict[str, Any],
    ) -> None:
        """Initialize a new Pragmatist.

        Args:
            name: The name of the board member.
            expertise_areas: List of expertise areas.
            personality_profile: Dict containing personality configuration.
            llm_config: Configuration for the LLM (temperature, etc.).
            implementation_focus: Primary implementation focus area.
            resource_context: Dict containing resource availability and constraints.
        """
        # Initialize role-specific context
        role_specific_context = {
            "implementation_focus": implementation_focus,
            "resource_context": resource_context,
            "implementation_plans": [],
            "feasibility_assessments": [],
            "action_items": [],
            "implementation_metrics": {
                "total_plans": 0,
                "completed_items": 0,
                "success_rate": 0.0,
            },
        }

        # Initialize base class with role-specific configuration
        super().__init__(
            name=name,
            role="Pragmatist",
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
            "confidence": 0.9,
            "metadata": {
                "role": "Pragmatist",
                "context_tokens": len(str(context)),
                "prompt_tokens": len(prompt),
                "implementation_focus": self.role_specific_context[
                    "implementation_focus"
                ],
            },
        }

    def create_implementation_plan(
        self, proposal: Dict[str, Any], timeline: str, dependencies: List[str]
    ) -> Dict[str, Any]:
        """Create a practical implementation plan.

        Args:
            proposal: The proposal to implement.
            timeline: Expected implementation timeline.
            dependencies: List of implementation dependencies.

        Returns:
            Dict containing the implementation plan.
        """
        plan = {
            "proposal": proposal,
            "timeline": timeline,
            "dependencies": dependencies,
            "phases": [],
            "resource_requirements": {},
            "risk_mitigation": [],
            "status": "draft",
            "timestamp": datetime.now().isoformat(),
        }

        self.role_specific_context["implementation_plans"].append(plan)
        self.role_specific_context["implementation_metrics"]["total_plans"] += 1

        return plan

    def assess_feasibility(
        self, proposal: Dict[str, Any], constraints: List[str]
    ) -> Dict[str, Any]:
        """Assess the feasibility of a proposal.

        Args:
            proposal: The proposal to assess.
            constraints: List of constraints to consider.

        Returns:
            Dict containing the feasibility assessment.
        """
        assessment = {
            "proposal": proposal,
            "constraints": constraints,
            "feasibility_score": 0.0,
            "practical_challenges": [],
            "resource_gaps": [],
            "recommendations": [],
            "timestamp": datetime.now().isoformat(),
        }

        self.role_specific_context["feasibility_assessments"].append(assessment)
        return assessment

    def create_action_items(
        self, plan: Dict[str, Any], assignees: List[str]
    ) -> List[Dict[str, Any]]:
        """Break down a plan into specific action items.

        Args:
            plan: The implementation plan.
            assignees: List of people to assign tasks to.

        Returns:
            List of action items.
        """
        action_items = []
        for phase in plan.get("phases", []):
            items = self._break_down_phase(phase, assignees)
            action_items.extend(items)

        self.role_specific_context["action_items"].extend(action_items)
        return action_items

    def update_action_status(
        self, item_id: str, new_status: str, completion_notes: Optional[str] = None
    ) -> None:
        """Update the status of an action item.

        Args:
            item_id: ID of the action item.
            new_status: New status of the item.
            completion_notes: Optional notes about completion.
        """
        for item in self.role_specific_context["action_items"]:
            if item.get("id") == item_id:
                item["status"] = new_status
                if completion_notes:
                    item["completion_notes"] = completion_notes
                if new_status == "completed":
                    self.role_specific_context["implementation_metrics"][
                        "completed_items"
                    ] += 1
                break

        # Update success rate
        total_items = len(self.role_specific_context["action_items"])
        if total_items > 0:
            completed = self.role_specific_context["implementation_metrics"][
                "completed_items"
            ]
            self.role_specific_context["implementation_metrics"]["success_rate"] = (
                completed / total_items
            )

    def _break_down_phase(
        self, phase: Dict[str, Any], assignees: List[str]
    ) -> List[Dict[str, Any]]:
        """Break down a phase into specific action items.

        Args:
            phase: The phase to break down.
            assignees: List of potential assignees.

        Returns:
            List of action items for the phase.
        """
        # This is a placeholder - actual implementation would be more sophisticated
        items = []
        for i, task in enumerate(phase.get("tasks", [])):
            items.append(
                {
                    "id": f"{phase['id']}-{i+1}",
                    "phase": phase["id"],
                    "task": task,
                    "assignee": assignees[i % len(assignees)],
                    "status": "pending",
                    "dependencies": [],
                    "estimated_effort": "1d",
                    "created_at": datetime.now().isoformat(),
                }
            )
        return items
