# Agentory

Agentory is an AI-powered assistant designed to answer questions, calculate inventory, and streamline insights for warehouse operations. It features a modern web UI (Next.js/TypeScript) and a Python backend that leverages LLMs and connects to warehouse data sources.

## Features

- **Conversational AI**: Interact with an AI agent to get warehouse insights through natural language.
- **Inventory Queries**: Ask about inventory, projected stock, capacities, and more.
- **Multi-Warehouse Support**: Easily switch queries between different warehouse locations.
- **Backend Intelligence**: Uses OpenAI (Azure) models for intent classification, SQL planning, summarization, and direct data retrieval.
- **Extensible**: Modular backend with components for intent classification, SQL generation, and summarization.

## Tech Stack

- **Frontend**: Next.js, TypeScript, React
- **Backend**: Python (FastAPI, OpenAI SDK, dotenv)
- **AI Models**: Azure OpenAI (GPT-based)
- **Others**: Virtualenv for Python dependencies

## Getting Started

### Prerequisites

- Node.js (for the frontend)
- Python 3.11+ (for the backend)
- Access to Azure OpenAI and environment variables for API keys

### Frontend (Next.js)

```bash
# Install dependencies
npm install

# Start the development server
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### Backend (Python)

```bash
cd agent-backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set up .env file with your Azure OpenAI credentials
python agent.py
```

### Connecting Frontend and Backend

The frontend sends chat requests to the backend at `http://localhost:8000/chat`. Make sure both servers are running.

## Project Structure

```
agentory/
├── agent-backend/           # Python backend with agent logic
│   ├── agent.py             # Main entry point for AI agent
│   ├── intent_classifier.py # Intent classification utility
│   ├── sql_planner.py       # SQL planner for database queries
│   ├── summarizer.py        # For summarizing responses
│   └── venv/                # Python virtual environment
├── src/
│   └── pages/
│       └── index.tsx        # Next.js frontend (main UI)
└── README.md
```

## Example Questions

- “For material MAT-0152, what is its shelf life?”
- “How much net quantity of outbound in Singapore warehouse this week?”
- “What is the projected inventory in Singapore today?”
