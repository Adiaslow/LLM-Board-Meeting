# llm_board_meeting/roles/functional/secretary.py

"""
Secretary implementation for the LLM Board Meeting system.

This module implements the Secretary role, responsible for documenting key points,
managing context hierarchy, and maintaining knowledge continuity between sessions.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import json

from llm_board_meeting.roles.base_llm_member import BaseLLMMember
from llm_board_meeting.context_management.manager import ContextManager
from llm_board_meeting.context_management.entry import ContextEntry


class Secretary(BaseLLMMember):
    """Secretary board member implementation.

    The Secretary is responsible for:
    - Documenting key points and decisions
    - Managing context hierarchy and information flow
    - Producing meeting minutes and summaries
    - Maintaining knowledge continuity between sessions
    - Tracking action items and follow-ups
    """

    def __init__(
        self,
        member_id: str,
        role_specific_context: Dict[str, Any],
        expertise_areas: List[str],
        personality_profile: Dict[str, Any],
        llm_config: Dict[str, Any],
        meeting_type: str,
        documentation_level: str,
        key_tracking_areas: List[str],
    ) -> None:
        """Initialize a new Secretary.

        Args:
            member_id: Unique identifier for the board member
            role_specific_context: Role-specific configuration and context
            expertise_areas: List of expertise areas
            personality_profile: Dict containing personality configuration
            llm_config: Configuration for the LLM (temperature, etc.)
            meeting_type: Type of meeting being documented
            documentation_level: Level of detail required
            key_tracking_areas: Areas requiring special attention
        """
        # Update role-specific context with additional fields
        role_specific_context.update(
            {
                "meeting_type": meeting_type,
                "documentation_level": documentation_level,
                "key_tracking_areas": key_tracking_areas,
                "key_points": [],
                "action_items": [],
                "decisions": [],
                "documentation_metrics": {
                    "total_key_points": 0,
                    "action_items_tracked": 0,
                    "decisions_recorded": 0,
                },
            }
        )

        # Initialize base class with role-specific configuration
        super().__init__(
            member_id=member_id,
            role="Secretary",
            expertise_areas=expertise_areas,
            personality_profile=personality_profile,
            role_specific_context=role_specific_context,
            llm_config=llm_config,
        )

        # Initialize the Context Management System
        context_config = {
            "active_discussion": {
                "max_entries": 50,
                "max_tokens": 8000,
                "retention_policy": "time",
            },
            "key_points": {
                "max_entries": 100,
                "max_tokens": 12000,
                "retention_policy": "importance",
            },
            "meeting_framework": {
                "max_entries": 20,
                "max_tokens": 4000,
                "retention_policy": "manual",
            },
            "persistent_knowledge": {
                "max_entries": 200,
                "max_tokens": 16000,
                "retention_policy": "importance",
            },
        }
        self.context_manager = ContextManager(config=context_config)

        # Initialize context layers
        self.context_manager.add_entry(
            content=f"Meeting Type: {meeting_type}\nDocumentation Level: {documentation_level}",
            source="system",
            layer="meeting_framework",
            metadata={"importance": 1.0},
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
            "confidence": 0.95,
            "metadata": {
                "role": "Secretary",
                "context_tokens": len(str(context)),
                "prompt_tokens": len(prompt),
                "meeting_type": self.role_specific_context["meeting_type"],
            },
        }

    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming message.

        Args:
            message: The message to process.

        Returns:
            Dict containing the response.
        """
        formatted_context = self._format_context({"message": message})
        response = await self.generate_response(
            context=formatted_context, prompt=json.dumps(message)
        )
        return response

    async def contribute_to_discussion(
        self, topic: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Contribute to the discussion by providing documentation and context.

        Args:
            topic: The current topic of discussion
            context: Current meeting context

        Returns:
            Dict containing the contribution and metadata
        """
        formatted_context = self._format_context(context)
        contribution = await self.generate_response(
            context=formatted_context,
            prompt=f"Document and provide context for: {topic}",
        )
        return contribution

    def record_key_point(
        self,
        topic: str,
        point: str,
        context: Dict[str, Any],
        source: str,
        importance: float,
    ) -> None:
        """Record a key discussion point.

        Args:
            topic: The topic being discussed.
            point: The key point to record.
            context: Relevant context for the point.
            source: Source of the point (e.g., board member).
            importance: Importance score (0-1).
        """
        # Add to context management system
        self.context_manager.add_entry(
            content=point,
            source=source,
            layer="active_discussion",
            metadata={
                "topic": topic,
                "context": context,
                "type": "key_point",
                "importance": importance,
            },
        )

        if importance >= 0.7:  # High importance points are promoted
            entry = ContextEntry(
                content=point,
                source=source,
                timestamp=datetime.now(),
                importance=importance,
                metadata={"topic": topic, "context": context, "type": "key_point"},
            )
            self.context_manager.promote_entry(entry, "key_points")

        # Update internal tracking
        self.role_specific_context["key_points"].append(
            {
                "topic": topic,
                "point": point,
                "context": context,
                "source": source,
                "importance": importance,
                "timestamp": datetime.now().isoformat(),
            }
        )
        self.role_specific_context["documentation_metrics"]["total_key_points"] += 1

    def track_action_item(
        self,
        topic: str,
        action: str,
        assignee: str,
        due_date: str,
        dependencies: List[str],
        priority: str,
    ) -> None:
        """Record an action item.

        Args:
            topic: The topic the action relates to.
            action: Description of the action required.
            assignee: Person/role responsible.
            due_date: Expected completion date.
            dependencies: List of dependent actions/items.
            priority: Priority level of the action.
        """
        # Create action item entry
        action_item = {
            "topic": topic,
            "action": action,
            "assignee": assignee,
            "due_date": due_date,
            "dependencies": dependencies,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
            "status": "open",
        }

        # Add to context management system
        importance = 0.8 if priority.lower() == "high" else 0.6
        self.context_manager.add_entry(
            content=f"Action Item: {action} (Assignee: {assignee})",
            source=self.member_id,
            layer="key_points",
            metadata={
                "type": "action_item",
                "action_details": action_item,
                "importance": importance,
            },
        )

        # Update internal tracking
        self.role_specific_context["action_items"].append(action_item)
        self.role_specific_context["documentation_metrics"]["action_items_tracked"] += 1

    def record_decision(
        self,
        topic: str,
        decision: str,
        rationale: str,
        stakeholders: List[str],
        implications: Dict[str, Any],
    ) -> None:
        """Record a decision made during the meeting.

        Args:
            topic: The topic of the decision.
            decision: The decision made.
            rationale: Reasoning behind the decision.
            stakeholders: Affected stakeholders.
            implications: Dict of decision implications.
        """
        # Create decision record
        decision_record = {
            "topic": topic,
            "decision": decision,
            "rationale": rationale,
            "stakeholders": stakeholders,
            "implications": implications,
            "timestamp": datetime.now().isoformat(),
            "status": "recorded",
        }

        # Add to context management system
        self.context_manager.add_entry(
            content=f"Decision: {decision}\nRationale: {rationale}",
            source=self.member_id,
            layer="key_points",
            metadata={
                "type": "decision",
                "decision_details": decision_record,
                "importance": 0.9,  # Decisions are highly important
            },
        )

        # Add to persistent knowledge for long-term reference
        self.context_manager.add_knowledge(
            content=f"Decision on {topic}: {decision}",
            metadata={
                "type": "decision",
                "decision_details": decision_record,
            },
        )

        # Update internal tracking
        self.role_specific_context["decisions"].append(decision_record)
        self.role_specific_context["documentation_metrics"]["decisions_recorded"] += 1

    def update_meeting_framework(
        self,
        current_topic: str,
        phase: str,
        time_remaining: int,
        next_topics: List[str],
    ) -> None:
        """Update the meeting framework information.

        Args:
            current_topic: Currently discussed topic.
            phase: Current meeting phase.
            time_remaining: Time remaining in minutes.
            next_topics: Upcoming topics.
        """
        framework_update = {
            "current_topic": current_topic,
            "phase": phase,
            "time_remaining": time_remaining,
            "next_topics": next_topics,
            "timestamp": datetime.now().isoformat(),
        }

        self.context_manager.update_framework(
            content=f"Meeting Status: {current_topic} ({phase})",
            metadata=framework_update,
        )

    def create_meeting_summary(
        self,
        topics_covered: List[str],
        key_outcomes: List[Dict[str, Any]],
        next_steps: List[str],
        discussion_highlights: Dict[str, List[str]],
    ) -> Dict[str, Any]:
        """Create a comprehensive meeting summary.

        Args:
            topics_covered: List of topics discussed.
            key_outcomes: List of main outcomes.
            next_steps: List of follow-up actions.
            discussion_highlights: Dict mapping topics to highlights.

        Returns:
            Dict containing the meeting summary.
        """
        # Get summaries from context management system
        active_summary = self.context_manager.get_layer_summary("active_discussion")
        key_points_summary = self.context_manager.get_layer_summary("key_points")
        framework_summary = self.context_manager.get_layer_summary("meeting_framework")

        summary = {
            "meeting_type": self.role_specific_context["meeting_type"],
            "topics_covered": topics_covered,
            "key_outcomes": key_outcomes,
            "next_steps": next_steps,
            "discussion_highlights": discussion_highlights,
            "decisions": [
                d
                for d in self.role_specific_context["decisions"]
                if d["status"] == "recorded"
            ],
            "action_items": [
                a
                for a in self.role_specific_context["action_items"]
                if a["status"] == "open"
            ],
            "key_points": sorted(
                self.role_specific_context["key_points"],
                key=lambda x: x["importance"],
                reverse=True,
            )[:5],
            "metrics": self.role_specific_context["documentation_metrics"],
            "context_summaries": {
                "active_discussion": active_summary,
                "key_points": key_points_summary,
                "framework": framework_summary,
            },
        }

        # Store summary in persistent knowledge
        self.context_manager.add_knowledge(
            content=f"Meeting Summary: {topics_covered}",
            metadata={"type": "meeting_summary", "summary": summary},
        )

        return summary

    def get_documentation_summary(self) -> Dict[str, Any]:
        """Get a summary of documentation activities.

        Returns:
            Dict containing documentation summary.
        """
        # Get current context from all layers
        active_summary = self.context_manager.get_layer_summary("active_discussion")
        key_points_summary = self.context_manager.get_layer_summary("key_points")
        framework_summary = self.context_manager.get_layer_summary("meeting_framework")
        knowledge_summary = self.context_manager.get_layer_summary(
            "persistent_knowledge"
        )

        return {
            "total_key_points": self.role_specific_context["documentation_metrics"][
                "total_key_points"
            ],
            "open_action_items": [
                item
                for item in self.role_specific_context["action_items"]
                if item["status"] == "open"
            ],
            "recent_decisions": self.role_specific_context["decisions"][-5:],
            "metrics": self.role_specific_context["documentation_metrics"],
            "documentation_analysis": self._analyze_documentation_patterns(),
            "context_summaries": {
                "active_discussion": active_summary,
                "key_points": key_points_summary,
                "framework": framework_summary,
                "knowledge": knowledge_summary,
            },
        }

    def search_context(
        self, query: str, layers: Optional[List[str]] = None
    ) -> List[ContextEntry]:
        """Search for relevant context entries.

        Args:
            query: The search query.
            layers: Optional list of layers to search in.

        Returns:
            List of relevant context entries.
        """
        return self.context_manager.search_context(query, layers)

    def get_current_context(self) -> Dict[str, str]:
        """Get the current context from all layers.

        Returns:
            Dict mapping layer names to their summaries.
        """
        # Get summaries from each layer
        active_summary = self.context_manager.get_layer_summary("active_discussion")
        key_points_summary = self.context_manager.get_layer_summary("key_points")
        framework_summary = self.context_manager.get_layer_summary("meeting_framework")
        knowledge_summary = self.context_manager.get_layer_summary(
            "persistent_knowledge"
        )

        return {
            "active_discussion": active_summary,
            "key_points": key_points_summary,
            "meeting_framework": framework_summary,
            "persistent_knowledge": knowledge_summary,
        }

    def _analyze_documentation_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in documentation.

        Returns:
            Dict containing documentation pattern analysis.
        """
        # Get summaries from each layer
        active_summary = self.context_manager.get_layer_summary("active_discussion")
        key_points_summary = self.context_manager.get_layer_summary("key_points")
        framework_summary = self.context_manager.get_layer_summary("meeting_framework")
        knowledge_summary = self.context_manager.get_layer_summary(
            "persistent_knowledge"
        )

        # Extract key themes from summaries if they exist
        key_themes = []
        if isinstance(key_points_summary, dict):
            key_themes = key_points_summary.get("key_themes", [])

        return {
            "key_themes": key_themes,
            "priority_actions": [
                action
                for action in self.role_specific_context["action_items"]
                if action["priority"] == "high" and action["status"] == "open"
            ],
            "decision_categories": self._categorize_decisions(),
            "documentation_coverage": self._calculate_coverage(),
            "context_analysis": {
                "active_discussion": active_summary,
                "key_points": key_points_summary,
                "framework": framework_summary,
                "knowledge": knowledge_summary,
            },
        }

    def _categorize_decisions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize decisions by topic.

        Returns:
            Dict mapping topics to lists of decisions.
        """
        categories: Dict[str, List[Dict[str, Any]]] = {}
        for decision in self.role_specific_context["decisions"]:
            topic = decision["topic"]
            if topic not in categories:
                categories[topic] = []
            categories[topic].append(decision)
        return categories

    def _calculate_coverage(self) -> Dict[str, float]:
        """Calculate documentation coverage metrics.

        Returns:
            Dict containing coverage metrics.
        """
        tracking_areas = set(self.role_specific_context["key_tracking_areas"])
        covered_areas = set()

        # Check coverage in key points
        for point in self.role_specific_context["key_points"]:
            if point["topic"] in tracking_areas:
                covered_areas.add(point["topic"])

        # Check coverage in decisions
        for decision in self.role_specific_context["decisions"]:
            if decision["topic"] in tracking_areas:
                covered_areas.add(decision["topic"])

        return {
            "topics_coverage": (
                len(covered_areas) / len(tracking_areas) if tracking_areas else 1.0
            ),
            "decisions_coverage": (
                len(self.role_specific_context["decisions"])
                / len(self.role_specific_context["key_points"])
                if self.role_specific_context["key_points"]
                else 0.0
            ),
            "actions_coverage": (
                len(
                    [
                        a
                        for a in self.role_specific_context["action_items"]
                        if a["status"] == "open"
                    ]
                )
                / len(self.role_specific_context["key_points"])
                if self.role_specific_context["key_points"]
                else 0.0
            ),
        }

    async def analyze_discussion(
        self, discussion_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze discussion history from a documentation perspective.

        Args:
            discussion_history: List of discussion entries to analyze.

        Returns:
            Dict containing documentation analysis and insights.
        """
        formatted_context = self._format_context(
            {"discussion_history": discussion_history}
        )
        analysis = await self.generate_response(
            context=formatted_context,
            prompt="Analyze the discussion from a documentation perspective",
        )

        # Add key points and decisions to context
        for entry in discussion_history:
            if entry.get("type") == "key_point":
                self.record_key_point(
                    topic=entry.get("topic", "general"),
                    point=entry.get("content", ""),
                    context={"source": entry.get("source")},
                    source=entry.get("source", "unknown"),
                    importance=entry.get("importance", 0.5),
                )
            elif entry.get("type") == "decision":
                self.record_decision(
                    topic=entry.get("topic", "general"),
                    decision=entry.get("content", ""),
                    rationale=entry.get("rationale", ""),
                    stakeholders=entry.get("stakeholders", []),
                    implications=entry.get("implications", {}),
                )

        return {
            **analysis,
            "documentation_metrics": self.role_specific_context[
                "documentation_metrics"
            ],
            "key_points": len(self.role_specific_context["key_points"]),
            "decisions": len(self.role_specific_context["decisions"]),
        }

    async def summarize_content(
        self, content: Dict[str, Any], summary_type: str
    ) -> Dict[str, Any]:
        """Summarize content with a focus on documentation and context preservation.

        Args:
            content: The content to summarize
            summary_type: Type of summary requested

        Returns:
            Dict containing the documentation-focused summary
        """
        formatted_context = self._format_context(
            {"content": content, "summary_type": summary_type}
        )
        summary = await self.generate_response(
            context=formatted_context,
            prompt=f"Provide a {summary_type} summary with focus on documentation",
        )

        # Add summary to appropriate context layer based on type
        if summary_type == "key_point":
            self.record_key_point(
                topic=content.get("topic", "general"),
                point=summary.get("content", ""),
                context={"source": "summarization"},
                source="Secretary",
                importance=0.7,
            )
        elif summary_type == "decision":
            self.record_decision(
                topic=content.get("topic", "general"),
                decision=summary.get("content", ""),
                rationale=summary.get("rationale", "Auto-generated summary"),
                stakeholders=content.get("stakeholders", []),
                implications=content.get("implications", {}),
            )

        return {
            **summary,
            "context_added": True,
            "summary_type": summary_type,
            "documentation_status": "recorded",
        }

    async def validate_proposal(
        self, proposal: Dict[str, Any], criteria: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate a proposal from a documentation perspective.

        Args:
            proposal: The proposal to validate
            criteria: The criteria to validate against

        Returns:
            Dict containing validation results and documentation assessment
        """
        formatted_context = self._format_context(
            {"proposal": proposal, "criteria": criteria}
        )
        validation = await self.generate_response(
            context=formatted_context,
            prompt="Validate this proposal from a documentation perspective",
        )
        return validation
