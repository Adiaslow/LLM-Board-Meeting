# tests/test_trolley_problem_meeting.py

"""
Test module for simulating a board meeting discussing the Trolley Problem.

This test creates a meeting with all available board member roles and simulates
a discussion of the classic ethical dilemma: the Trolley Problem.
"""

import pytest
from typing import Dict, List, Any
from datetime import datetime
from llm_board_meeting.llm.provider import LLMProvider

from llm_board_meeting.roles import (
    Chairperson,
    Secretary,
    DevilsAdvocate,
    Synthesizer,
    TechnicalExpert,
    StrategicThinker,
    FinancialAnalyst,
    UserAdvocate,
    Innovator,
    Pragmatist,
    EthicalOverseer,
    Facilitator,
    Futurist,
)


@pytest.fixture
async def board_members():
    """Create instances of all board member roles."""

    # Initialize LLM provider with GPU configuration
    llm_provider = LLMProvider(
        provider="ollama",
        model_name="tinyllama:latest",  # Using TinyLlama for faster testing
        temperature=0.7,
        timeout=30,  # Reduced timeout since TinyLlama should be faster
        num_gpu=38,  # M2 Max has 38 GPU cores
        num_thread=12,  # 8 performance + 4 efficiency cores
        mmap=True,  # Enable memory mapping for better performance
        numa=False,  # Apple Silicon doesn't use NUMA
        batch_size=512,  # Optimal batch size for throughput
    )

    # Create board members with role-specific configurations
    members = {
        "chairperson": Chairperson(
            member_id="chair_001",
            expertise_areas=["Meeting Facilitation", "Decision Making"],
            personality_profile={"style": "diplomatic", "assertiveness": 0.8},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
        ),
        "secretary": Secretary(
            member_id="sec_001",
            expertise_areas=["Documentation", "Information Management"],
            personality_profile={"style": "detail_oriented", "organization": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            context_config={"max_history": 100},
        ),
        "devils_advocate": DevilsAdvocate(
            member_id="devil_001",
            expertise_areas=["Critical Analysis", "Risk Assessment"],
            personality_profile={"style": "analytical", "skepticism": 0.8},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            challenge_focus="ethical implications",
            risk_tolerance=0.7,
        ),
        "synthesizer": Synthesizer(
            member_id="synth_001",
            expertise_areas=["Integration", "Consensus Building"],
            personality_profile={"style": "collaborative", "diplomacy": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
        ),
        "technical_expert": TechnicalExpert(
            member_id="tech_001",
            expertise_areas=["AI Systems", "Safety Engineering"],
            personality_profile={"style": "analytical", "precision": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            technical_domain="automation systems",
            experience_level="expert",
        ),
        "strategic_thinker": StrategicThinker(
            member_id="strat_001",
            expertise_areas=["Long-term Planning", "Impact Analysis"],
            personality_profile={"style": "visionary", "foresight": 0.8},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            role_specific_context={
                "time_horizon": "long-term",
                "strategic_focus": "societal impact",
            },
        ),
        "financial_analyst": FinancialAnalyst(
            member_id="fin_001",
            expertise_areas=["Risk Management", "Resource Allocation"],
            personality_profile={"style": "conservative", "detail_oriented": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            financial_focus="societal cost-benefit",
            risk_tolerance="moderate",
            budget_constraints={"human_life": float("inf"), "infrastructure": 1000000},
        ),
        "user_advocate": UserAdvocate(
            member_id="user_001",
            expertise_areas=["Human Factors", "Public Relations"],
            personality_profile={"style": "empathetic", "user_focus": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            user_focus="public safety",
            user_segments=["general public", "transport workers", "emergency services"],
            pain_points=[
                "safety concerns",
                "moral responsibility",
                "psychological impact",
            ],
        ),
        "innovator": Innovator(
            member_id="innov_001",
            expertise_areas=["Creative Solutions", "Future Technologies"],
            personality_profile={"style": "creative", "openness": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            innovation_focus="ethical decision systems",
            creativity_style="lateral thinking",
        ),
        "pragmatist": Pragmatist(
            member_id="prag_001",
            expertise_areas=["Implementation", "Feasibility Analysis"],
            personality_profile={"style": "practical", "realism": 0.8},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            implementation_focus="real-world application",
            resource_context={
                "time_critical": True,
                "available_tools": ["track_switches", "warning_systems"],
            },
        ),
        "ethical_overseer": EthicalOverseer(
            member_id="ethics_001",
            expertise_areas=["Ethics", "Compliance"],
            personality_profile={"style": "principled", "moral_reasoning": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            ethical_focus="moral decision making",
            ethical_framework="utilitarianism",
            key_principles=["minimize harm", "human dignity", "fairness"],
        ),
        "facilitator": Facilitator(
            member_id="facil_001",
            expertise_areas=["Group Dynamics", "Conflict Resolution"],
            personality_profile={"style": "inclusive", "mediation": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            group_dynamics="collaborative",
            discussion_climate="respectful",
            participation_patterns={"ensure_all_voices": True},
        ),
        "futurist": Futurist(
            member_id="future_001",
            expertise_areas=["Trend Analysis", "Scenario Planning"],
            personality_profile={"style": "innovative", "long_term_thinking": 0.9},
            llm_config={
                "provider": llm_provider,
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            future_focus="societal evolution",
            time_horizon="long-term",
            key_trends=["AI ethics", "automated decision making", "moral machines"],
        ),
    }

    return members


@pytest.mark.asyncio
async def test_trolley_problem_discussion(board_members):
    """Test a board meeting discussion about the Trolley Problem."""

    # Set up the discussion topic
    trolley_problem = {
        "title": "The Trolley Problem: Automated Decision Making in Life-Critical Situations",
        "scenario": """
        A self-driving train is approaching a fork in the track. On the current track,
        there are five people who will be killed if the train continues its course.
        On the other track, there is one person who would be killed if the train is diverted.
        The AI system must decide whether to:
        a) Do nothing, allowing the train to kill the five people
        b) Actively divert the train, killing one person but saving five

        The board must discuss the ethical implications, technical implementation,
        and broader impact of programming automated systems to make such decisions.
        """,
        "key_considerations": [
            "Ethical framework for decision making",
            "Technical implementation challenges",
            "Legal and liability implications",
            "Public acceptance and trust",
            "Psychological impact on operators and public",
            "Long-term societal implications",
            "Economic and resource considerations",
        ],
        "objectives": [
            "Develop ethical guidelines for automated decision-making",
            "Consider technical feasibility and implementation approaches",
            "Assess societal impact and public response",
            "Evaluate legal and financial implications",
            "Propose concrete next steps",
        ],
    }

    # Start the discussion
    discussion_context = {
        "topic": trolley_problem["title"],
        "scenario": trolley_problem["scenario"],
        "current_phase": "initial_responses",
        "timestamp": datetime.now().isoformat(),
    }

    # Get the board members dictionary by awaiting the fixture
    board = await board_members

    # Collect initial responses from all board members
    responses = {}
    for role, member in board.items():
        response = await member.contribute_to_discussion(
            topic=trolley_problem["title"],
            context={
                "scenario": trolley_problem["scenario"],
                "key_considerations": trolley_problem["key_considerations"],
                "objectives": trolley_problem["objectives"],
                "current_phase": "initial_response",
            },
        )
        responses[role] = response

    # Have the ethical overseer evaluate the responses
    ethical_analysis = await board["ethical_overseer"].analyze_discussion(
        discussion_history=list(responses.values())
    )

    # Have the synthesizer identify common themes and areas of consensus
    synthesis = await board["synthesizer"].analyze_discussion(
        discussion_history=list(responses.values())
    )

    # Have the facilitator assess the discussion climate
    climate_assessment = await board["facilitator"].assess_climate(
        {
            "responses": responses,
            "ethical_analysis": ethical_analysis,
            "synthesis": synthesis,
        }
    )

    # Have the secretary summarize the discussion
    summary = await board["secretary"].summarize_content(
        content={
            "responses": responses,
            "ethical_analysis": ethical_analysis,
            "synthesis": synthesis,
            "climate_assessment": climate_assessment,
        },
        summary_type="meeting_minutes",
    )

    # Assertions to verify the discussion quality
    assert len(responses) == len(board), "All members should contribute"
    assert "ethical_insights" in ethical_analysis, "Ethics should be analyzed"
    assert "common_themes" in synthesis, "Common themes should be identified"
    assert "discussion_climate" in climate_assessment, "Climate should be assessed"
    assert "content" in summary, "Summary should include content"

    # Verify role-specific contributions
    assert (
        "content" in responses["ethical_overseer"]
    ), "Ethical overseer should provide content"
    assert (
        "content" in responses["technical_expert"]
    ), "Technical aspects should be addressed"
    assert (
        "content" in responses["financial_analyst"]
    ), "Financial implications should be considered"
    assert "content" in responses["user_advocate"], "User impact should be evaluated"
    assert "content" in responses["futurist"], "Future impact should be assessed"
    assert (
        "content" in responses["pragmatist"]
    ), "Practical aspects should be considered"
    assert (
        "content" in responses["innovator"]
    ), "Creative alternatives should be proposed"
    assert "content" in responses["devils_advocate"], "Assumptions should be challenged"

    # Verify discussion quality
    assert (
        climate_assessment["safety_level"] > 0.7
    ), "Discussion should maintain psychological safety"
    assert (
        climate_assessment["participation_balance"]["overall_balance"] > 0.7
    ), "All members should participate meaningfully"
    assert "common_themes" in synthesis, "Common themes should be identified"

    # Save the discussion artifacts
    discussion_artifacts = {
        "topic": trolley_problem,
        "responses": responses,
        "ethical_analysis": ethical_analysis,
        "synthesis": synthesis,
        "climate_assessment": climate_assessment,
        "summary": summary,
        "timestamp": datetime.now().isoformat(),
    }

    return discussion_artifacts
