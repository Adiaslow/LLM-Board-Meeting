# llm_board_meeting/roles/base_llm_member.py

"""
Base LLM Member implementation for the LLM Board Meeting system.

This module provides the concrete LLM-based implementation of the BoardMember interface,
serving as the base class for all LLM-powered board member roles. It implements common
LLM-specific functionality while adhering to the BoardMember interface contract.
"""

from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import json
from datetime import datetime

from llm_board_meeting.core.board_member import BoardMember
from llm_board_meeting.roles.config.role_prompts import (
    get_role_prompts,
    format_prompt_template,
)


class BaseLLMMember(BoardMember):
    """Base class for all LLM-powered board members.

    This class provides concrete LLM-specific implementations of the BoardMember interface,
    along with additional functionality common to all LLM-based roles. All LLM-powered
    board member roles should inherit from this class rather than BoardMember directly.
    """

    def __init__(
        self,
        member_id: str,
        role: str,
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        role_specific_context: Dict[str, Any],
        llm_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize a new LLM-powered board member.

        Args:
            member_id: Unique identifier for the board member
            role: The role of the board member
            expertise_areas: List of expertise areas
            personality_profile: Dict containing personality configuration
            role_specific_context: Dict containing role-specific context variables
            llm_config: Configuration for the LLM (temperature, etc.)
        """
        super().__init__(
            name=member_id,
            role=role,
            expertise_areas=expertise_areas,
            personality_profile=personality_profile,
            role_specific_context=role_specific_context,
            llm_config=llm_config,
        )

        self.member_id = member_id
        self.role = role
        self.role_specific_context = role_specific_context
        self.llm_config = llm_config or {}

        # Initialize state tracking
        self.conversation_history: List[Dict[str, Any]] = []
        self.assessments: List[Dict[str, Any]] = []
        self.confidence_scores: List[float] = []

        # Get role-specific prompt templates
        self.prompt_config = get_role_prompts(role)

        # Set up LLM configuration with defaults
        self.temperature = self.llm_config.get("temperature", 0.7)
        self.max_tokens = self.llm_config.get("max_tokens", 1000)

    def _get_base_system_prompt(self) -> str:
        """Get the base system prompt for the role.

        Returns:
            String containing the base system prompt.
        """
        context = {"role_name": self.role, **self.role_specific_context}
        return format_prompt_template(self.prompt_config["base_prompt"], context)

    def _get_role_specific_prompt(self) -> str:
        """Get role-specific prompt modifications.

        Returns:
            String containing role-specific prompt additions.
        """
        template = self.prompt_config["role_specific_prompt"]["context_template"]
        return template.format(**self.role_specific_context)

    def _get_evaluation_prompt(self) -> str:
        """Get the evaluation-specific system prompt.

        Returns:
            String containing the system prompt for evaluations.
        """
        template = self.prompt_config["evaluation_prompt"]
        prompt = template["intro"].format(**self.role_specific_context) + "\n"

        for i, point in enumerate(template["points"], 1):
            prompt += f"{i}. {point}\n"

        if "conclusion" in template:
            prompt += f"\n{template['conclusion'].format(**self.role_specific_context)}"

        return prompt

    def _get_feedback_prompt(self) -> str:
        """Get the feedback-specific system prompt.

        Returns:
            String containing the system prompt for feedback.
        """
        template = self.prompt_config["feedback_prompt"]
        prompt = template["intro"].format(**self.role_specific_context) + "\n"

        for i, point in enumerate(template["points"], 1):
            prompt += f"{i}. {point}\n"

        if "conclusion" in template:
            prompt += f"\n{template['conclusion'].format(**self.role_specific_context)}"

        return prompt

    @abstractmethod
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
        pass

    async def generate_response(
        self, context: Dict[str, Any], prompt: str, **kwargs
    ) -> Dict[str, Any]:
        """Generate a response based on the given context and prompt.

        Args:
            context: The current context including meeting state and history.
            prompt: The specific prompt for this interaction.
            **kwargs: Additional keyword arguments for response generation.

        Returns:
            Dict containing the response and metadata.
        """
        formatted_context = self._format_context(context)
        system_prompt = self._get_base_system_prompt()

        response = await self._generate_llm_response(
            system_prompt=system_prompt,
            context=formatted_context,
            prompt=prompt,
            **kwargs,
        )

        self.conversation_history.append(
            {
                "prompt": prompt,
                "response": response,
                "timestamp": datetime.now().isoformat(),
            }
        )

        if "confidence" in response:
            self.confidence_scores.append(response["confidence"])
            self.confidence_score = response["confidence"]

        return response

    async def evaluate_proposal(
        self, proposal: Dict[str, Any], criteria: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate a proposal based on given criteria.

        Args:
            proposal: The proposal to evaluate.
            criteria: The criteria to evaluate against.

        Returns:
            Dict mapping criteria to scores.
        """
        evaluation_prompt = self._get_evaluation_prompt()
        context = {
            "proposal": proposal,
            "criteria": criteria,
        }

        response = await self._generate_llm_response(
            system_prompt=evaluation_prompt,
            context=context,
            prompt=json.dumps(proposal),
        )

        self.assessments.append(
            {
                "type": "proposal_evaluation",
                "proposal": proposal,
                "evaluation": response,
                "timestamp": datetime.now().isoformat(),
            }
        )

        # Convert response to criteria scores
        scores = {}
        for criterion, details in response.get("criteria_evaluation", {}).items():
            scores[criterion] = float(details.get("score", 0.0))

        return scores

    async def provide_feedback(
        self, target_content: Dict[str, Any], feedback_type: str
    ) -> Dict[str, Any]:
        """Provide feedback on specific content.

        Args:
            target_content: The content to provide feedback on.
            feedback_type: The type of feedback requested.

        Returns:
            Dict containing structured feedback.
        """
        feedback_prompt = self._get_feedback_prompt()
        context = {
            "target_content": target_content,
            "feedback_type": feedback_type,
        }

        response = await self._generate_llm_response(
            system_prompt=feedback_prompt,
            context=context,
            prompt=json.dumps(target_content),
        )

        self.assessments.append(
            {
                "type": "feedback",
                "feedback_type": feedback_type,
                "target": target_content,
                "feedback": response,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return response

    def get_confidence_score(self) -> float:
        """Get the average confidence score for recent responses.

        Returns:
            Float representing the average confidence score.
        """
        if not self.confidence_scores:
            return 0.0
        return sum(self.confidence_scores[-10:]) / len(self.confidence_scores[-10:])

    def _format_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format the context for role-specific needs.

        Args:
            context: Raw context dictionary.

        Returns:
            Formatted context dictionary.
        """
        return {
            "name": self.member_id,
            "role": self.role,
            "expertise_areas": self.expertise_areas,
            "personality_profile": self.personality_profile,
            "conversation_history": self.conversation_history[-5:],
            "recent_assessments": self.assessments[-3:],
            "confidence_score": self.get_confidence_score(),
            **self.role_specific_context,
            **context,
        }

    def get_member_summary(self) -> Dict[str, Any]:
        """Get a summary of the board member's state and activities.

        Returns:
            Dict containing member summary.
        """
        return {
            "name": self.member_id,
            "role": self.role,
            "expertise_areas": self.expertise_areas,
            "recent_interactions": self.conversation_history[-5:],
            "recent_assessments": self.assessments[-3:],
            "confidence_score": self.get_confidence_score(),
            "role_specific_context": self.role_specific_context,
        }
