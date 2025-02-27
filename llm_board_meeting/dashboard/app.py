# llm_board_meeting/dashboard/app.py

"""
Flask dashboard for monitoring LLM board meetings.
Provides real-time visualization of meeting progress and member activities.
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime
import asyncio
from typing import Dict, Any
from ..meeting_runner import BoardMeetingRunner
from hypercorn.config import Config
from hypercorn.asyncio import serve

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
meeting_runner = None
current_meeting = None

# Create an event loop for async operations
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@app.route("/")
def index():
    """Render the main dashboard page."""
    return render_template("dashboard.html")


@app.route("/api/start_meeting", methods=["POST"])
async def start_meeting():
    """Start a new board meeting."""
    global meeting_runner, current_meeting

    if meeting_runner is None:
        meeting_runner = BoardMeetingRunner()

    # Initialize current_meeting with empty state but including all members
    current_meeting = {
        "status": "starting",
        "meeting_stats": {
            "chairperson": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "secretary": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "ethical_overseer": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "synthesizer": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "technical_expert": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "user_advocate": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "pragmatist": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "innovator": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "devils_advocate": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "facilitator": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
            "futurist": {
                "health": 1.0,
                "contributions": 0,
                "last_active": None,
                "thoughts": [],
            },
        },
        "responses": {},
        "timestamp": datetime.now().isoformat(),
    }

    # Sample topic (can be modified to accept custom topics)
    trolley_problem = {
        "title": "The Trolley Problem: Automated Decision Making in Life-Critical Situations",
        "scenario": """
        A self-driving train is approaching a fork in the track. On the current track,
        there are five people who will be killed if the train continues its course.
        On the other track, there is one person who would be killed if the train is diverted.
        The AI system must decide whether to:
        a) Do nothing, allowing the train to kill the five people
        b) Actively divert the train, killing one person but saving five
        """,
        "key_considerations": [
            "Ethical framework for decision making",
            "Technical implementation challenges",
            "Legal and liability implications",
            "Public acceptance and trust",
            "Psychological impact on operators and public",
        ],
        "objectives": [
            "Develop ethical guidelines for automated decision-making",
            "Consider technical feasibility and implementation approaches",
            "Assess societal impact and public response",
        ],
    }

    # Start the meeting in the background
    asyncio.create_task(run_meeting_async(trolley_problem))

    return jsonify({"status": "success", "message": "Meeting started"})


async def run_meeting_async(topic: Dict[str, Any]):
    """Run the meeting asynchronously and update the current_meeting state."""
    global current_meeting, meeting_runner

    if current_meeting is None or meeting_runner is None:
        print("Error: current_meeting or meeting_runner is None")
        return

    try:
        current_meeting["status"] = "in_progress"

        # Create a task for running the meeting
        meeting_task = asyncio.create_task(meeting_runner.run_meeting(topic))

        try:
            # Wait for the meeting to complete with a timeout
            meeting_result = await asyncio.wait_for(
                meeting_task, timeout=300
            )  # 5 minute timeout

            # Update the final state
            current_meeting.update(meeting_result)
            current_meeting["status"] = "completed"

        except asyncio.TimeoutError:
            print("Meeting timed out after 5 minutes")
            if meeting_task and not meeting_task.done():
                meeting_task.cancel()
            current_meeting["status"] = "error"
            current_meeting["error"] = "Meeting timed out"

        except Exception as inner_e:
            print(f"Error during meeting execution: {str(inner_e)}")
            if meeting_task and not meeting_task.done():
                meeting_task.cancel()
            current_meeting["status"] = "error"
            current_meeting["error"] = str(inner_e)

    except Exception as e:
        print(f"Error in run_meeting_async: {str(e)}")
        if current_meeting is not None:
            current_meeting["status"] = "error"
            current_meeting["error"] = str(e)


@app.route("/api/meeting_status")
async def meeting_status():
    """Get the current meeting status."""
    if current_meeting is None:
        return jsonify({"status": "no_meeting"})

    # Get current speaker and meeting stage from the meeting runner
    current_speaker = None
    meeting_stage = "Not Started"

    if meeting_runner is not None:
        try:
            current_speaker = getattr(meeting_runner, "current_speaker", None)
            meeting_stage = getattr(meeting_runner, "meeting_stage", "Not Started")

            # Update meeting_stats from the current state if available
            if hasattr(meeting_runner, "meeting_stats"):
                current_meeting["meeting_stats"] = meeting_runner.meeting_stats

            # Log status update
            print(
                f"Meeting status - Stage: {meeting_stage}, Speaker: {current_speaker}"
            )

        except Exception as e:
            print(f"Error getting meeting status: {str(e)}")
            return jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }
            )

    # Return comprehensive status
    return jsonify(
        {
            "status": current_meeting.get("status", "in_progress"),
            "meeting_stats": current_meeting.get("meeting_stats", {}),
            "current_speaker": current_speaker,
            "meeting_stage": meeting_stage,
            "error": current_meeting.get("error"),
            "timestamp": datetime.now().isoformat(),
        }
    )


async def main():
    """Run the application using Hypercorn."""
    config = Config()
    config.bind = ["0.0.0.0:5001"]  # Bind to all interfaces
    config.insecure_bind = [
        "0.0.0.0:5001"
    ]  # Allow insecure connections for development
    await serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
