# LLM Board Meeting Dashboard

A real-time dashboard for monitoring AI board meetings with multiple LLM-powered board members discussing complex topics.

## Features

- Real-time monitoring of board member activities
- Health status indicators for each member
- Contribution tracking and recent thoughts display
- Interactive dashboard with responsive design
- GPU-accelerated LLM processing (optimized for Apple Silicon M2 Max)

## Prerequisites

- Python 3.8+
- Ollama with TinyLlama model installed
- macOS with Apple Silicon M2 Max (for optimal GPU acceleration)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/llm-board-meeting.git
cd llm-board-meeting
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Ollama and download the TinyLlama model:

```bash
# Install Ollama from https://ollama.ai
ollama pull tinyllama:latest
```

## Running the Dashboard

1. Start the Ollama service:

```bash
ollama serve
```

2. In a new terminal, start the Flask dashboard:

```bash
python -m llm_board_meeting.dashboard.app
```

3. Open your browser and navigate to:

```
http://localhost:5000
```

4. Click "Start New Meeting" to begin a board meeting simulation.

## Board Members

The dashboard includes the following AI board members:

- Chairperson
- Secretary
- Devil's Advocate
- Synthesizer
- Technical Expert
- Strategic Thinker
- Financial Analyst
- User Advocate
- Innovator
- Pragmatist
- Ethical Overseer
- Facilitator
- Futurist

Each member has:

- Specialized role and expertise
- Real-time health monitoring
- Contribution tracking
- Recent thoughts display

## Development

To run tests:

```bash
pytest tests/
```

To run a standalone meeting without the dashboard:

```bash
python -m llm_board_meeting.meeting_runner
```

## License

MIT License - See LICENSE file for details
