# 🏭 Agentory

**Agentory** is an intelligent assistant designed to answer questions, calculate inventory, and streamline insights for warehouse operations.

Built with a modern web UI (**Next.js + TypeScript**) and a Python backend using **FastAPI**, Agentory leverages **Large Language Models (LLMs)** from Azure OpenAI and connects directly to **live warehouse data (Azure SQL)**. It enables supply chain analysts, planners, and operations teams to get instant, natural-language answers from raw warehouse datasets — no SQL, no pivot tables, no delay.

Whether you're asking:

> “What is the projected inventory in Singapore on 31/12/2023?”

or:

> “How much outbound quantity left the Singapore warehouse this week?”

Agentory processes your intent, generates the appropriate SQL, runs it securely, summarizes the results, and returns a clear and concise answer — with an optional **Thinking Log** that shows every step of its reasoning.

## Features

- **Conversational AI**: Interact with an AI agent to get warehouse information through natural language.
- **Inventory Queries**: Ask about inventory, projected stock, capacities, and more.
- **Multi-Warehouse Support**: Easily switch queries between different warehouse locations.
- **Backend Intelligence**: Uses OpenAI (Azure) models for intent classification, SQL planning, summarization, and direct data retrieval.
- **Extensible**: Modular backend with components for intent classification, SQL generation, and SQL summarization.

## Tech Stack

- **Frontend**: Next.js, TypeScript, React
- **Backend**: Python (FastAPI, OpenAI SDK, dotenv)
- **AI Models**: Azure OpenAI (GPT-based)
- **Others**: Virtualenv for Python dependencies

## Getting Started

### Prerequisites

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
### 📁 Environment Variables Example

Create a `.env` in backend folder:

```env
# Azure OpenAI
AZURE_OPENAI_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-04-01-preview

AZURE_INTENT_CLASSIFIER_ASSISTANT_ID=asst_xxx
AZURE_SQL_PLANNER_ASSISTANT_ID=asst_xxx
AZURE_SUMMARIZER_ASSISTANT_ID=asst_xxx

# Azure SQL
AZURE_SQL_SERVER=your_server.database.windows.net
AZURE_SQL_DATABASE=your_db
AZURE_SQL_USERNAME=username
AZURE_SQL_PASSWORD=password

```

### Connecting Frontend and Backend

The frontend sends chat requests to the backend at `http://localhost:8000/chat`. Make sure both servers are running.

## Project Structure

```
agentory/
├── agent-backend/
│   ├── main.py               # FastAPI entrypoint
│   ├── agent.py              # Main entry point for AI agent
│   ├── intent_classifier.py  # Intent classifier utility
│   ├── sql_planner.py        # SQL planner agent (GPT)
│   ├── query_executor.py     # Connect to Azure SQL + run query
│   ├── summarizer.py         # Natural human language responses
│   ├── upload_Sql.py         # Upload CSV to SQL
│   └── .env                  # Environment Variables
│   └── venv/                 # Python virtual environment
├── src/
│   └── pages/index.tsx       # Chat UI (Next.js)
└── README.md

```

## Example Questions

- “For material MAT-0152, what is its shelf life?”
- “How much net quantity of outbound in Singapore warehouse this week?”
- “What is the projected inventory in Singapore today?”

>  Built for Bootcathon 2025 — GenAI Track 

## System Instructions & Prompt Location
The core instruction prompts (also known as system prompts) for the agent are configured directly inside Azure OpenAI Assistants.

This means:
The behavior of each agent tool — including the Intent Classifier, SQL Planner, and Summarizer — is controlled via predefined instructions inside Azure.
These prompts define the agent’s role, response format, expected output structure (e.g., SQL string, JSON intent), and reasoning style.
The local code only handles message routing and logging — actual “thinking” is done through assistants hosted in Azure.
