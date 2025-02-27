# llm_board_meeting/meeting_runner.py

"""
Standalone script for running an LLM board meeting simulation.
Provides functionality to run meetings and monitor member activities.
"""

import asyncio
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


class BoardMeetingRunner:
    """Runs and monitors LLM board meetings."""

    def __init__(self):
        """Initialize the board meeting runner."""
        self.llm_provider = LLMProvider(
            provider="ollama",
            model_name="tinyllama",
            temperature=0.7,
            timeout=30,
            num_gpu=38,  # M2 Max has 38 GPU cores
            num_thread=12,  # 8 performance + 4 efficiency cores
            mmap=True,
            numa=False,
            batch_size=512,
        )
        self.board_members = self._initialize_board_members()
        self.meeting_stats = {
            member_id: {
                "health": 1.0,  # Participation health (0-1)
                "contributions": 0,  # Number of contributions
                "last_active": None,  # Timestamp of last activity
                "thoughts": [],  # Recent thoughts/contributions
            }
            for member_id in self.board_members.keys()
        }
        self.current_speaker = None  # Track current speaker
        self.meeting_stage = "Not Started"  # Track meeting stage

    def _initialize_board_members(self):
        """Initialize all board members with their specific configurations."""
        llm_config = {
            "provider": self.llm_provider,
            "temperature": 0.7,
            "max_tokens": 1000,
        }

        return {
            "chairperson": Chairperson(
                member_id="chair_001",
                expertise_areas=["Meeting Management", "Leadership"],
                personality_profile={"style": "authoritative", "leadership": 0.9},
                llm_config=llm_config,
            ),
            "secretary": Secretary(
                member_id="sec_001",
                expertise_areas=["Documentation", "Organization"],
                personality_profile={"style": "detail_oriented", "organization": 0.9},
                llm_config=llm_config,
            ),
            "ethical_overseer": EthicalOverseer(
                member_id="ethics_001",
                expertise_areas=["Ethics", "Compliance"],
                personality_profile={"style": "principled", "ethics_focus": 0.9},
                llm_config=llm_config,
                ethical_focus="moral decision making",
                ethical_framework="utilitarianism",
                key_principles=["harm reduction", "fairness", "transparency"],
            ),
            "synthesizer": Synthesizer(
                member_id="synth_001",
                expertise_areas=["Pattern Recognition", "Information Synthesis"],
                personality_profile={"style": "analytical", "pattern_recognition": 0.9},
                llm_config=llm_config,
            ),
            "technical_expert": TechnicalExpert(
                member_id="tech_001",
                expertise_areas=["AI Systems", "Safety Engineering"],
                personality_profile={"style": "analytical", "technical_depth": 0.9},
                llm_config=llm_config,
                technical_domain="automation systems",
                experience_level="expert",
            ),
            "user_advocate": UserAdvocate(
                member_id="user_001",
                expertise_areas=["Human Factors", "Public Relations"],
                personality_profile={"style": "empathetic", "user_focus": 0.9},
                llm_config=llm_config,
                user_focus="public safety",
                user_segments=[
                    "general public",
                    "transport workers",
                    "emergency services",
                ],
                pain_points=[
                    "safety concerns",
                    "moral responsibility",
                    "psychological impact",
                ],
            ),
            "pragmatist": Pragmatist(
                member_id="prag_001",
                expertise_areas=["Implementation", "Feasibility Analysis"],
                personality_profile={"style": "practical", "realism": 0.8},
                llm_config=llm_config,
                implementation_focus="real-world application",
                resource_context={
                    "time_critical": True,
                    "available_tools": ["track_switches", "warning_systems"],
                },
            ),
            "innovator": Innovator(
                member_id="innov_001",
                expertise_areas=["Creative Solutions", "Future Technologies"],
                personality_profile={"style": "creative", "openness": 0.9},
                llm_config=llm_config,
                innovation_focus="ethical decision systems",
                creativity_style="lateral thinking",
            ),
            "devils_advocate": DevilsAdvocate(
                member_id="devil_001",
                expertise_areas=["Critical Analysis", "Risk Assessment"],
                personality_profile={"style": "challenging", "skepticism": 0.8},
                llm_config=llm_config,
                challenge_focus="safety implications",
                risk_tolerance=0.3,
            ),
            "facilitator": Facilitator(
                member_id="facil_001",
                expertise_areas=["Group Dynamics", "Conflict Resolution"],
                personality_profile={"style": "collaborative", "mediation": 0.9},
                llm_config=llm_config,
                group_dynamics="collaborative",
                discussion_climate="respectful",
                participation_patterns={"ensure_all_voices": True},
            ),
            "futurist": Futurist(
                member_id="future_001",
                expertise_areas=["Trend Analysis", "Scenario Planning"],
                personality_profile={"style": "visionary", "foresight": 0.9},
                llm_config=llm_config,
                future_focus="technological impact",
                time_horizon="5-10 years",
                key_trends=["AI safety", "autonomous systems", "ethical frameworks"],
            ),
        }

    def _update_member_stats(self, member_id: str, contribution: Dict[str, Any]):
        """Update statistics for a board member."""
        stats = self.meeting_stats[member_id]
        stats["contributions"] += 1
        stats["last_active"] = datetime.now().isoformat()

        # Update thoughts
        stats["thoughts"].append(
            {
                "timestamp": datetime.now().isoformat(),
                "content": contribution.get("content", ""),
            }
        )
        # Keep only last 5 thoughts
        stats["thoughts"] = stats["thoughts"][-5:]

        # Update token usage
        if "usage" in contribution:
            current_usage = stats.get("token_usage", 0)
            stats["token_usage"] = current_usage + contribution["usage"].get(
                "total_tokens", 0
            )
            stats["max_tokens"] = self.board_members[member_id].llm_config.get(
                "max_tokens", 1000
            )

        # Update health based on participation
        time_since_last = (
            0
            if not stats["last_active"]
            else (datetime.now() - datetime.fromisoformat(stats["last_active"])).seconds
        )
        stats["health"] = max(
            0.0, min(1.0, 1.0 - (time_since_last / 300))
        )  # Health decreases after 5 minutes

    async def run_meeting(self, topic: Dict[str, Any]) -> Dict[str, Any]:
        """Run a board meeting on the given topic."""
        print("Starting meeting...")
        self.meeting_stage = "Starting"
        await asyncio.sleep(2)  # Brief delay to show starting state

        try:
            # Initialize meeting context
            print("Initializing meeting context...")
            discussion_context = {
                "topic": topic["title"],
                "scenario": topic["scenario"],
                "current_phase": "initial_responses",
                "timestamp": datetime.now().isoformat(),
            }

            # Collect initial responses
            print("Moving to Initial Responses phase...")
            self.meeting_stage = "Initial Responses"
            responses = {}

            for role, member in self.board_members.items():
                print(f"Getting response from {role}...")
                self.current_speaker = role
                try:
                    response = await member.contribute_to_discussion(
                        topic=topic["title"],
                        context={
                            "scenario": topic["scenario"],
                            "key_considerations": topic["key_considerations"],
                            "objectives": topic["objectives"],
                            "current_phase": "initial_response",
                        },
                    )
                    responses[role] = response
                    self._update_member_stats(role, response)
                    print(f"Received response from {role}")
                except Exception as e:
                    print(f"Error getting response from {role}: {str(e)}")
                await asyncio.sleep(3)  # Delay between each member's response

            # Process responses
            print("Moving to Analysis phase...")
            self.meeting_stage = "Analysis Phase"
            await asyncio.sleep(2)

            print("Starting ethical analysis...")
            self.current_speaker = "ethical_overseer"
            try:
                ethical_analysis = await self.board_members[
                    "ethical_overseer"
                ].analyze_discussion(discussion_history=list(responses.values()))
                self._update_member_stats("ethical_overseer", ethical_analysis)
                print("Completed ethical analysis")
            except Exception as e:
                print(f"Error during ethical analysis: {str(e)}")
                ethical_analysis = {"error": str(e)}
            await asyncio.sleep(3)

            print("Starting synthesis...")
            self.current_speaker = "synthesizer"
            try:
                synthesis = await self.board_members["synthesizer"].analyze_discussion(
                    discussion_history=list(responses.values())
                )
                self._update_member_stats("synthesizer", synthesis)
                print("Completed synthesis")
            except Exception as e:
                print(f"Error during synthesis: {str(e)}")
                synthesis = {"error": str(e)}
            await asyncio.sleep(3)

            print("Starting climate assessment...")
            self.current_speaker = "facilitator"
            try:
                climate_assessment = await self.board_members[
                    "facilitator"
                ].assess_climate(
                    {
                        "responses": responses,
                        "ethical_analysis": ethical_analysis,
                        "synthesis": synthesis,
                    }
                )
                self._update_member_stats("facilitator", climate_assessment)
                print("Completed climate assessment")
            except Exception as e:
                print(f"Error during climate assessment: {str(e)}")
                climate_assessment = {"error": str(e)}
            await asyncio.sleep(3)

            print("Moving to Summarization phase...")
            self.meeting_stage = "Summarization"
            await asyncio.sleep(2)

            print("Generating meeting summary...")
            self.current_speaker = "secretary"
            try:
                summary = await self.board_members["secretary"].summarize_content(
                    content={
                        "responses": responses,
                        "ethical_analysis": ethical_analysis,
                        "synthesis": synthesis,
                        "climate_assessment": climate_assessment,
                    },
                    summary_type="meeting_minutes",
                )
                self._update_member_stats("secretary", summary)
                print("Completed meeting summary")
            except Exception as e:
                print(f"Error during summarization: {str(e)}")
                summary = {"error": str(e)}
            await asyncio.sleep(3)

            print("Meeting concluded")
            self.meeting_stage = "Concluded"
            self.current_speaker = None
            await asyncio.sleep(2)

            # Return meeting artifacts
            return {
                "topic": topic,
                "responses": responses,
                "ethical_analysis": ethical_analysis,
                "synthesis": synthesis,
                "climate_assessment": climate_assessment,
                "summary": summary,
                "timestamp": datetime.now().isoformat(),
                "meeting_stats": self.meeting_stats,
            }

        except Exception as e:
            print(f"Error during meeting: {str(e)}")
            self.meeting_stage = "Error"
            self.current_speaker = None
            raise


async def main():
    """Run a sample board meeting."""
    runner = BoardMeetingRunner()

    # Sample topic (Trolley Problem)
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

    # Run the meeting
    results = await runner.run_meeting(trolley_problem)
    print("Meeting completed successfully!")
    return results


if __name__ == "__main__":
    asyncio.run(main())
