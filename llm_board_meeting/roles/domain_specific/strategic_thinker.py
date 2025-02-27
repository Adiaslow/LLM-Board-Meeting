# llm_board_meeting/roles/domain_specific/strategic_thinker.py

"""
Strategic Thinker implementation for the LLM Board Meeting system.

This module implements the Strategic Thinker role, responsible for long-term
strategic analysis, opportunity identification, and future planning.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime

from ..base_llm_member import BaseLLMMember


class StrategicThinker(BaseLLMMember):
    """Strategic Thinker board member implementation.

    The Strategic Thinker is responsible for:
    - Long-term strategic analysis
    - Identifying opportunities and threats
    - Connecting ideas to broader goals
    - Evaluating competitive landscape
    - Future scenario planning
    """

    def __init__(
        self,
        member_id: str,
        role_specific_context: Dict[str, Any],
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        llm_config: Dict[str, Any],
    ) -> None:
        """Initialize a new Strategic Thinker.

        Args:
            member_id: Unique identifier for the board member.
            role_specific_context: Role-specific configuration and context.
            expertise_areas: List of areas of expertise.
            personality_profile: Dict containing personality traits and preferences.
            llm_config: Configuration for the LLM.
        """
        super().__init__(
            member_id=member_id,
            role="StrategicThinker",
            expertise_areas=expertise_areas,
            personality_profile=personality_profile,
            role_specific_context=role_specific_context,
            llm_config=llm_config,
        )

        # Initialize tracking collections
        self.strategic_insights: List[Dict[str, Any]] = []
        self.scenario_analyses: List[Dict[str, Any]] = []
        self.opportunity_threats: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
            "opportunities": {},
            "threats": {},
        }

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming message in the context of strategic thinking.

        Args:
            message: The message to process.

        Returns:
            Dict containing the processed response.
        """
        formatted_context = self._format_context(message)
        response = await self.generate_response(
            context=formatted_context, prompt=message["message"]
        )

        # Record any strategic insights from the response
        if "strategic_insight" in response:
            self.add_strategic_insight(
                topic=message.get("current_topic", "general"),
                insight=response["strategic_insight"],
                implications=response.get("implications", []),
                time_frame=self.role_specific_context.get("time_horizon", "long-term"),
            )

        return response

    async def contribute_to_discussion(
        self, topic: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Contribute to the discussion from a strategic perspective.

        Args:
            topic: The current topic of discussion.
            context: Current meeting context.

        Returns:
            Dict containing the contribution and metadata.
        """
        formatted_context = self._format_context(context)
        contribution = await self.generate_response(
            context=formatted_context,
            prompt=f"Provide strategic perspective on: {topic}",
        )

        return {
            **contribution,
            "strategic_focus": self.role_specific_context.get("strategic_focus"),
            "time_horizon": self.role_specific_context.get("time_horizon"),
        }

    async def analyze_discussion(
        self, discussion_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze discussion history from a strategic perspective.

        Args:
            discussion_history: List of discussion entries to analyze.

        Returns:
            Dict containing strategic analysis and insights.
        """
        formatted_context = self._format_context(
            {"discussion_history": discussion_history}
        )
        analysis = await self.generate_response(
            context=formatted_context,
            prompt="Analyze the discussion from a strategic perspective",
        )

        return {**analysis, "strategic_metrics": self.get_strategic_summary()}

    def _format_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Format context for strategic analysis.

        Args:
            context: Raw context dictionary.

        Returns:
            Formatted context dictionary.
        """
        base_context = super()._format_context(context)

        return {
            **base_context,
            "recent_insights": self.strategic_insights[-5:],
            "active_scenarios": self.scenario_analyses[-3:],
            "opportunities_threats": self.opportunity_threats,
            "strategic_objectives": context.get("strategic_objectives", {}),
            "competitive_landscape": context.get("competitive_landscape", {}),
            "market_trends": context.get("market_trends", []),
        }

    # Role-specific helper methods
    def add_strategic_insight(
        self, topic: str, insight: str, implications: List[str], time_frame: str
    ) -> None:
        """Record a strategic insight.

        Args:
            topic: The topic of the insight.
            insight: The strategic insight.
            implications: List of strategic implications.
            time_frame: Time frame for the implications.
        """
        self.strategic_insights.append(
            {
                "topic": topic,
                "insight": insight,
                "implications": implications,
                "time_frame": time_frame,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def add_scenario_analysis(
        self,
        scenario_name: str,
        description: str,
        drivers: List[str],
        implications: Dict[str, Any],
        probability: float,
    ) -> None:
        """Add a scenario analysis.

        Args:
            scenario_name: Name of the scenario.
            description: Description of the scenario.
            drivers: Key drivers of the scenario.
            implications: Dict of implications by area.
            probability: Estimated probability (0-1).
        """
        self.scenario_analyses.append(
            {
                "name": scenario_name,
                "description": description,
                "drivers": drivers,
                "implications": implications,
                "probability": probability,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def record_opportunity_threat(
        self, category: str, item: str, impact: str, time_frame: str
    ) -> None:
        """Record an opportunity or threat.

        Args:
            category: Either "opportunities" or "threats".
            item: The opportunity or threat to record.
            impact: Description of potential impact.
            time_frame: Time frame for the impact.
        """
        if time_frame not in self.opportunity_threats[category]:
            self.opportunity_threats[category][time_frame] = []

        self.opportunity_threats[category][time_frame].append(
            {"item": item, "impact": impact, "timestamp": datetime.now().isoformat()}
        )

    def get_strategic_summary(self) -> Dict[str, Any]:
        """Get a summary of strategic analysis.

        Returns:
            Dict containing strategic analysis summary.
        """
        return {
            "focus_area": self.role_specific_context.get("strategic_focus"),
            "time_horizon": self.role_specific_context.get("time_horizon"),
            "recent_insights": self.strategic_insights[-5:],
            "active_scenarios": self.scenario_analyses[-3:],
            "opportunity_threat_analysis": self.opportunity_threats,
            "metrics": {
                "total_insights": len(self.strategic_insights),
                "total_scenarios": len(self.scenario_analyses),
                "opportunities_identified": sum(
                    len(v) for v in self.opportunity_threats["opportunities"].values()
                ),
                "threats_identified": sum(
                    len(v) for v in self.opportunity_threats["threats"].values()
                ),
            },
        }

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
        return await super()._generate_llm_response(
            system_prompt, context, prompt, **kwargs
        )

    async def summarize_content(
        self, content: Dict[str, Any], summary_type: str
    ) -> Dict[str, Any]:
        """Summarize content from a strategic perspective.

        Args:
            content: The content to summarize.
            summary_type: Type of summary requested.

        Returns:
            Dict containing the strategic summary.
        """
        system_prompt = """Summarize the following content from a strategic perspective, 
        focusing on long-term implications and strategic alignment."""

        summary_prompt = f"""Please provide a strategic summary of:
        {content}
        
        Focus on:
        1. Long-term implications
        2. Strategic alignment
        3. Key opportunities and threats
        4. Critical success factors"""

        response = await self._generate_llm_response(
            system_prompt=system_prompt, context=content, prompt=summary_prompt
        )

        return {
            "summary": response.get("content", ""),
            "focus_area": self.role_specific_context.get("strategic_focus"),
            "time_horizon": self.role_specific_context.get("time_horizon"),
            "timestamp": datetime.now().isoformat(),
        }

    async def validate_proposal(
        self, proposal: Dict[str, Any], criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate a proposal against strategic criteria.

        Args:
            proposal: The proposal to validate.
            criteria: The criteria to validate against.

        Returns:
            Dict containing validation results and strategic assessment.
        """
        system_prompt = """Evaluate this proposal from a strategic perspective, 
        considering long-term viability and strategic alignment."""

        validation_prompt = f"""Please evaluate the following proposal:
        {proposal}
        
        Against these criteria:
        {criteria}
        
        Consider:
        1. Strategic alignment
        2. Long-term viability
        3. Resource implications
        4. Competitive advantage
        5. Risk factors"""

        response = await self._generate_llm_response(
            system_prompt=system_prompt,
            context={"proposal": proposal, "criteria": criteria},
            prompt=validation_prompt,
        )

        return {
            "is_valid": True,  # This should be determined based on the response
            "strategic_assessment": response.get("content", ""),
            "focus_area": self.role_specific_context.get("strategic_focus"),
            "time_horizon": self.role_specific_context.get("time_horizon"),
            "timestamp": datetime.now().isoformat(),
        }
