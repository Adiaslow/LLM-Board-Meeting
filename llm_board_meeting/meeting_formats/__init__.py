# llm_board_meeting/meeting_formats/__init__.py

"""
Meeting format implementations for the LLM Board Meeting system.

This package provides different meeting format structures, each designed for
specific types of discussions and decision-making processes:

1. Brainstorming Format:
   - Collaborative idea generation and evaluation
   - Phases: Problem framing, divergent thinking, clustering, evaluation

2. Decision Analysis Format:
   - Structured evaluation of options against criteria
   - Phases: Options enumeration, criteria definition, assessment, sensitivity analysis

3. Problem Solving Format:
   - Sequential approach to resolving challenges
   - Phases: Problem definition, root cause analysis, solution generation, implementation

4. Retrospective Format:
   - Analysis of past work to extract lessons
   - Phases: Data gathering, analysis, insight generation, action planning

5. Strategic Planning Format:
   - Forward-looking framework development
   - Phases: Environmental analysis, vision setting, strategy formulation, execution
"""

from llm_board_meeting.meeting_formats.base_format import MeetingFormat
from llm_board_meeting.meeting_formats.brainstorming import BrainstormingFormat
from llm_board_meeting.meeting_formats.decision_analysis import (
    DecisionAnalysisFormat,
)
from llm_board_meeting.meeting_formats.problem_solving import ProblemSolvingFormat
from llm_board_meeting.meeting_formats.retrospective import RetrospectiveFormat
from llm_board_meeting.meeting_formats.strategic_planning import (
    StrategicPlanningFormat,
)

__all__ = [
    "MeetingFormat",
    "BrainstormingFormat",
    "DecisionAnalysisFormat",
    "ProblemSolvingFormat",
    "RetrospectiveFormat",
    "StrategicPlanningFormat",
]
