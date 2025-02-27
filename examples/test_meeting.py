async def setup_test_meeting() -> Meeting:
    """Set up a test meeting with basic configuration."""

    # Initialize LLM provider with lightweight model
    llm_provider = LLMProvider(
        provider="ollama",
        model_name="tinyllama",  # Remove temperature from here
    )

    # Create board members
    strategic_thinker = StrategicThinker(
        member_id="st_1",
        role_specific_context={
            "strategic_focus": "product development",
            "time_horizon": "12 months",
        },
        expertise_areas=[
            "strategic planning",
            "market analysis",
            "competitive analysis",
        ],
        personality_profile={
            "communication_style": "analytical",
            "risk_tolerance": "moderate",
            "decision_making": "methodical",
        },
        llm_config={
            "provider": llm_provider,
            "temperature": 0.7,  # Temperature will be used in generate_response
            "max_tokens": 500,
        },
    )

    synthesizer = Synthesizer(
        member_id="syn_1",
        role_specific_context={
            "integration_focus": "cross-functional alignment",
            "stakeholder_groups": ["engineering", "product", "business"],
        },
        expertise_areas=["consensus building", "facilitation", "integration"],
        personality_profile={
            "communication_style": "collaborative",
            "risk_tolerance": "balanced",
            "decision_making": "inclusive",
        },
        llm_config={"provider": llm_provider, "temperature": 0.6, "max_tokens": 500},
    )

    secretary = Secretary(
        member_id="sec_1",
        role_specific_context={
            "meeting_type": "strategic planning",
            "documentation_level": "detailed",
            "key_tracking_areas": ["decisions", "action items", "strategic insights"],
        },
        expertise_areas=[
            "documentation",
            "meeting management",
            "information organization",
        ],
        personality_profile={
            "communication_style": "precise",
            "risk_tolerance": "conservative",
            "decision_making": "structured",
        },
        llm_config={"provider": llm_provider, "temperature": 0.3, "max_tokens": 500},
    )

    # ... rest of the code remains the same
