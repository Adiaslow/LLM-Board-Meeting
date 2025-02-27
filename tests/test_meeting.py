"""
Test script to demonstrate a basic LLM Board Meeting.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

from llm_board_meeting.core.meeting import Meeting
from llm_board_meeting.roles.domain_specific.strategic_thinker import StrategicThinker
from llm_board_meeting.roles.functional.synthesizer import Synthesizer
from llm_board_meeting.roles.functional.secretary import Secretary
from llm_board_meeting.llm.provider import LLMProvider


async def setup_test_meeting() -> Meeting:
    """Set up a test meeting with basic configuration."""

    # Initialize LLM provider with lightweight model
    llm_provider = LLMProvider(
        provider="ollama", model_name="tinyllama", temperature=0.7  # or "llama2:7b"
    )

    # Create board members
    strategic_thinker = StrategicThinker(
        member_id="StrategicThinker",
        role_specific_context={
            "strategic_focus": "product development",
            "planning_focus": "strategic planning",
            "key_objectives": [
                "Market expansion",
                "Product innovation",
                "Customer retention",
            ],
        },
        expertise_areas=["strategic planning", "business development"],
        personality_profile={
            "openness": 0.8,
            "conscientiousness": 0.7,
            "risk_tolerance": 0.6,
        },
        llm_config={"provider": llm_provider, "temperature": 0.7, "max_tokens": 500},
    )

    synthesizer = Synthesizer(
        member_id="Synthesizer",
        role_specific_context={
            "integration_focus": "cross-functional alignment",
            "stakeholder_groups": ["engineering", "product", "business"],
        },
        expertise_areas=["idea integration", "consensus building"],
        personality_profile={
            "openness": 0.8,
            "conscientiousness": 0.7,
            "collaboration": 0.9,
        },
        llm_config={"provider": llm_provider, "temperature": 0.6, "max_tokens": 500},
    )

    secretary = Secretary(
        member_id="Secretary",
        role_specific_context={
            "documentation_focus": "comprehensive",
            "information_hierarchy": ["decisions", "action_items", "insights"],
            "tracking_priorities": ["strategic", "operational", "technical"],
        },
        expertise_areas=["documentation", "information management"],
        personality_profile={
            "openness": 0.6,
            "conscientiousness": 0.9,
            "detail_orientation": 0.9,
            "analytical": 0.8,
            "collaborative": 0.7,
        },
        llm_config={"provider": llm_provider, "temperature": 0.3, "max_tokens": 500},
        meeting_type="strategic planning",
        documentation_level="detailed",
        key_tracking_areas=["decisions", "action items", "strategic insights"],
    )

    # Create meeting configuration
    meeting_config = {
        "format": "strategic_planning",
        "duration_minutes": 30,
        "requires_consensus": True,
        "topics": ["Q1 Product Roadmap", "Resource Allocation", "Market Positioning"],
    }

    # Initialize meeting
    meeting = Meeting(
        meeting_id=f"test_meeting_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        format_config=meeting_config,
        members=[strategic_thinker, synthesizer, secretary],
    )

    return meeting


async def run_test_meeting(meeting: Meeting) -> None:
    """Run a test meeting with sample topics."""

    print("\n=== Starting Meeting ===")
    # Start the meeting
    await meeting.start()
    print("✓ Meeting initialized successfully")
    print(f"Current state: {meeting.state.value}")

    # Process each topic
    topics = [
        {
            "name": "Q1 Product Roadmap",
            "context": {
                "current_status": "Planning phase",
                "key_objectives": [
                    "Feature A",
                    "Feature B",
                    "Performance improvements",
                ],
                "constraints": ["Budget", "Timeline", "Resources"],
            },
        },
        {
            "name": "Resource Allocation",
            "context": {
                "available_resources": {"engineers": 5, "designers": 2, "pm": 1},
                "priority_projects": ["Project X", "Project Y"],
                "timeline": "Q1 2024",
            },
        },
    ]

    for topic in topics:
        print(f"\n=== Processing Topic: {topic['name']} ===")
        print("Context provided:", topic["context"])

        try:
            print("Retrieving context from context manager...")
            result = await meeting.process_topic(topic["name"], topic["context"])
            print("✓ Topic processed successfully")

            print("\nContributions received:")
            for i, contribution in enumerate(result["contributions"], 1):
                print(f"\nContribution #{i}:")
                print(f"Source: {contribution.get('source', 'Unknown')}")
                content = contribution.get("content", "")
                print(
                    f"Content: {content[:100]}..."
                    if len(content) > 100
                    else f"Content: {content}"
                )
                print(f"Metadata: {contribution.get('metadata', {})}")

            if result.get("decisions"):
                print("\nDecisions made:")
                for decision in result["decisions"]:
                    print(f"- {decision}")

            # Add some action items
            print("\nAdding action items...")
            action_item = f"Follow up on {topic['name']} discussion points"
            await meeting.add_action_item(
                description=action_item,
                assignee="st_1",
                due_date="2024-01-31",
            )
            print(f"✓ Added action item: {action_item}")

        except Exception as e:
            print(f"\n❌ Error processing topic {topic['name']}:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("Current meeting state:", meeting.state.value)
            raise  # Re-raise the exception for full traceback

    print("\n=== Concluding Meeting ===")
    try:
        # Conclude the meeting
        summary = await meeting.conclude()

        print("\nMeeting Summary:")
        print(f"Duration: {summary['metrics']['duration']} seconds")
        print(f"Topics covered: {summary['metrics']['topics_covered']}")
        print(f"Decisions made: {summary['metrics']['decisions_made']}")

        print("\nAction Items:")
        for item in summary["action_items"]:
            print(f"- {item['description']} (Assignee: {item['assignee']})")

        print("\n✓ Meeting concluded successfully")

    except Exception as e:
        print("\n❌ Error concluding meeting:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("Final meeting state:", meeting.state.value)
        raise


async def main():
    """Main test function."""
    print("\n=== Setting Up Test Meeting ===")
    try:
        print("Initializing meeting components...")
        meeting = await setup_test_meeting()
        print("✓ Meeting setup completed")

        print("\nStarting test meeting...")
        await run_test_meeting(meeting)

    except Exception as e:
        print("\n❌ Fatal Error:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback

        print("\nFull traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
