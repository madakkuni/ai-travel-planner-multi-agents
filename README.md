# ✈️ AI Travel Planner — Multi-Agent System

> An AI-powered, multi-agent travel planning application that researches destinations, hotels, activities, and travel options, then produces a personalized itinerary with **guardrails and human-in-the-loop approval**.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-LLM%20Framework-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent%20Orchestration-orange)
![MCP](https://img.shields.io/badge/MCP-Tool%20Integration-purple)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

---

## 📌 Overview

**AI Travel Planner** is a multi-agent AI application designed to automate the travel planning process from a natural-language request to a personalized itinerary.

Instead of relying on a single LLM call, the application uses specialized agents coordinated through **LangGraph**.

The system can:

- Understand a user's travel request.
- Research the destination.
- Find hotels.
- Find attractions and activities.
- Research travel and transportation information.
- Combine research into an itinerary.
- Validate inputs and outputs using guardrails.
- Ask the user for approval or clarification before producing the final itinerary.
- Use MCP to connect agents with external tools such as web search.
- Run asynchronously for external API and MCP operations.
- Run locally or as Docker containers.

---

# 🏗️ Architecture

```text
                              User
                               |
                               v
                     ┌───────────────────┐
                     │ Streamlit UI      │
                     └─────────┬─────────┘
                               |
                               v
                     ┌───────────────────┐
                     │ FastAPI API       │
                     └─────────┬─────────┘
                               |
                               v
                     ┌───────────────────┐
                     │ Input Guardrails  │
                     └─────────┬─────────┘
                               |
                               v
                  ┌─────────────────────────┐
                  │    Supervisor Agent     │
                  │ Understand & Route Work │
                  └────────────┬────────────┘
                               |
             ┌─────────────────┼─────────────────┐
             |                 |                 |
             v                 v                 v
     ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
     │ Travel        │ │ Hotel Agent   │ │ Activity      │
     │ Research      │ │               │ │ Agent         │
     │ Agent         │ │               │ │               │
     └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
             |                 |                 |
             └─────────────────┼─────────────────┘
                               |
                               v
                    ┌─────────────────────┐
                    │ Itinerary Agent     │
                    │ Combine & Plan      │
                    └──────────┬──────────┘
                               |
                               v
                    ┌─────────────────────┐
                    │ Output Guardrails   │
                    └──────────┬──────────┘
                               |
                               v
                    ┌─────────────────────┐
                    │ Human-in-the-Loop   │
                    │ Review / Approve /  │
                    │ Modify              │
                    └──────────┬──────────┘
                               |
                         Approved?
                         /       \
                       No         Yes
                       |           |
                       v           v
                 Re-plan /     Final Draft
                 Clarify           |
                                   v
                              Final Output
```

---

# 🤖 Multi-Agent Design

The system separates responsibilities across specialized agents rather than putting the entire workflow into one prompt.

| Component | Responsibility |
|---|---|
| **Supervisor Agent** | Understand the user's request, identify required work, and route tasks to appropriate agents |
| **Travel Research Agent** | Research destination, transportation, travel information, and relevant trip details |
| **Hotel Agent** | Find hotels and extract useful hotel metadata |
| **Activity Agent** | Find attractions, places to visit, and activities |
| **Itinerary Agent** | Combine research results into a coherent, personalized itinerary |
| **Guardrails** | Validate inputs and outputs and protect the workflow from invalid or unsafe requests |
| **Human-in-the-Loop** | Allow the user to review, approve, reject, or request changes before the final itinerary is produced |

---

# 👤 Human-in-the-Loop

A key part of the architecture is **human approval before the final itinerary**.

The system does not blindly generate a final travel plan.

Instead:

```text
Agent Research
      |
      v
Draft Itinerary
      |
      v
Output Guardrails
      |
      v
Human Review
      |
      +---- Reject / Modify ----> Re-plan
      |
      +---- Approve -----------> Final Itinerary
```

The human can review information such as:

- Destination
- Travel dates / duration
- Hotels
- Activities
- Transportation
- Budget-related preferences
- Day-by-day itinerary

The user can then:

1. **Approve** the draft.
2. **Request changes**.
3. **Correct travel details**.
4. **Reject recommendations**.
5. **Ask the agents to re-plan**.

This creates a controlled workflow where AI performs the research and planning while the human remains responsible for the final decision.

---

# 🛡️ Guardrails

Guardrails are placed around the agent workflow rather than relying only on the LLM.

```text
User Input
    |
    v
Input Guardrails
    |
    v
Agent Workflow
    |
    v
Output Guardrails
    |
    v
Human Review
    |
    v
Final Output
```

### Input Guardrails

Potential validations include:

- Required travel information.
- Input format validation.
- Invalid or ambiguous destinations.
- Prompt injection detection.
- PII detection where appropriate.
- Request validation.
- Cost/rate controls.

### Output Guardrails

Potential validations include:

- Schema validation.
- Missing required fields.
- Invalid recommendations.
- Hallucinated information detection.
- Unsafe or irrelevant content.
- Duplicate results.
- Consistency between travel dates and itinerary.
- Validation before presenting results to the user.

---

# 🔄 End-to-End Workflow

Example user request:

```text
Plan a 5-day trip from Bangalore to Calicut.
I want good hotels and places to visit.
```

The workflow becomes:

```text
1. User Request
       |
       v
2. Input Guardrails
       |
       v
3. Supervisor Agent
       |
       +----> Travel Research Agent
       |
       +----> Hotel Agent
       |
       +----> Activity Agent
       |
       v
4. Research Results
       |
       v
5. Itinerary Agent
       |
       v
6. Draft Itinerary
       |
       v
7. Output Guardrails
       |
       v
8. Human Review
       |
       +---- Modify ----> Agents / Itinerary Agent
       |
       +---- Approve ---> Final Itinerary
```

---

# 🧠 Why Multi-Agent?

A single LLM prompt could technically generate a travel plan, but separating responsibilities provides better control and extensibility.

### Specialized responsibilities

Each agent focuses on a specific problem:

```text
Supervisor
    ↓
"Who should do this?"

Travel Research Agent
    ↓
"What do I need to know about the destination?"

Hotel Agent
    ↓
"Where should the user stay?"

Activity Agent
    ↓
"What should the user do?"

Itinerary Agent
    ↓
"How do I combine everything into a practical plan?"
```

This makes it easier to:

- Add new agents.
- Replace individual tools.
- Test agents independently.
- Add specialized prompts.
- Apply agent-specific guardrails.
- Scale the workflow.
- Debug failures.
- Improve individual capabilities without redesigning the entire system.

---

# 🔌 MCP Integration

The project uses **Model Context Protocol (MCP)** to connect AI agents with external tools.

Current integration uses Tavily MCP for web search.

```text
Agent
  |
  v
MCP Client
  |
  v
Tavily MCP Server
  |
  v
Search Tool
  |
  v
External Web Information
```

The MCP client discovers available tools and selects the required tool.

Example:

```text
Available MCP tools:
- tavily_search
- tavily_extract
- tavily_crawl
- tavily_map
- tavily_research
```

The current hotel workflow uses the search capability asynchronously.

```python
raw_results = await mcp_search_tool(search_query)
```

---

# 🕸️ LangGraph Orchestration

LangGraph is used to model the travel workflow as a graph of stateful nodes.

Conceptually:

```text
                    Supervisor
                         |
          ┌──────────────┼──────────────┐
          |              |              |
          v              v              v
       Travel          Hotel         Activity
      Research         Agent          Agent
          |              |              |
          └──────────────┼──────────────┘
                         |
                         v
                    Itinerary
                         |
                         v
                    Guardrails
                         |
                         v
                  Human Review
                         |
                    Approval?
                   /         \
                 No           Yes
                 |             |
                 v             v
              Re-plan       Final
```

The workflow maintains shared travel state between agents.

The graph is invoked asynchronously:

```python
result = await app.ainvoke(initial_state, config=config)
```

---

# 🏨 Hotel Agent

The Hotel Agent:

1. Builds a hotel search query.
2. Calls Tavily through MCP.
3. Receives raw search results.
4. Sends results to Azure OpenAI.
5. Extracts useful hotel metadata.
6. Returns normalized results.

Example output:

```json
{
  "hotels": [
    {
      "name": "Example Hotel",
      "location": "Calicut",
      "description": "Hotel description",
      "website": "https://example.com"
    }
  ]
}
```

The LLM is instructed to avoid inventing information and return `null` when data is unavailable.

---

# 🧩 Technology Stack

| Technology | Purpose |
|---|---|
| **Python 3.13** | Application runtime |
| **uv** | Dependency and environment management |
| **FastAPI** | Backend API |
| **Uvicorn** | ASGI server |
| **Streamlit** | Frontend |
| **LangChain** | LLM application framework |
| **LangGraph** | Multi-agent orchestration |
| **MCP** | External tool integration |
| **Tavily** | Web search |
| **Azure OpenAI** | LLM |
| **Docker** | Containerization |
| **Docker Compose** | Multi-service orchestration |

---

# 📁 Project Structure

```text
ai-travel-planner-multi-agents/
│
├── app/
│   ├── agents/
│   │   ├── supervisor_agent.py
│   │   ├── travel_research_agent.py
│   │   ├── hotel_agent.py
│   │   ├── activity_agent.py
│   │   └── itinerary_agent.py
│   │
│   ├── guardrails/
│   │   ├── input_guardrails.py
│   │   └── output_guardrails.py
│   │
│   ├── core/
│   │   ├── llm.py
│   │   └── logger.py
│   │
│   ├── mcp/
│   │   └── mcp_client.py
│   │
│   ├── prompts/
│   │   └── ...
│   │
│   ├── services/
│   │   └── ...
│   │
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── tests/
│
├── logs/
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

> Some agent and guardrail modules represent the target architecture and will be implemented progressively.

---

# ⚡ Async Architecture

External operations are handled asynchronously.

Example:

```python
async def hotel_agent(state):
    raw_results = await mcp_search_tool(search_query)
```

The service invokes LangGraph asynchronously:

```python
result = await app.ainvoke(initial_state, config=config)
```

The FastAPI endpoint is also asynchronous:

```python
@router.post("/travel")
async def create_travel_plan(request: TravelRequest):
    result = await process_travel_request(request.user_query)
```

This avoids coroutine serialization problems such as:

```text
TypeError: Object of type coroutine is not JSON serializable
```

---

# 🖥️ Local Development

## Prerequisites

- Python 3.13+
- Git
- uv
- Docker
- Docker Compose

## Clone

```bash
git clone <repository-url>
cd ai-travel-planner-multi-agents
```

## Create environment

```bash
uv venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```cmd
.venv\Scripts\activate
```

## Install dependencies

```bash
uv sync
```

Reproducible installation:

```bash
uv sync --frozen
```

---

# 🔐 Environment Variables & Secrets

Create a local `.env`:

```env
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_VERSION=<your-version>
AZURE_OPENAI_DEPLOYMENT=<your-deployment>

TAVILY_MCP_URL=<your-mcp-url>
```

Never commit the real `.env`.

Commit only:

```text
.env.example
```

For production, secrets should be injected at runtime rather than baked into the Docker image.

Recommended production approach:

```text
Azure Application
       |
       v
Managed Identity
       |
       v
Azure Key Vault
       |
       v
Runtime Secrets
```

---

# 🐳 Docker

The project intentionally uses **one Dockerfile** for both backend and frontend.

Docker Compose creates two services from the same image:

```text
                 Dockerfile
                     |
                     v
                Docker Image
                 /        \
                /          \
               v            v
          Backend         Frontend
          FastAPI         Streamlit
          :8000           :8501
```

Start:

```bash
docker compose up -d --build
```

Check:

```bash
docker compose ps
```

Logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

### Docker networking

The frontend communicates with the backend using:

```env
TRAVEL_API_URL=http://backend:8000
```

not:

```env
TRAVEL_API_URL=http://localhost:8000
```

because `localhost` inside the frontend container refers to the frontend container itself.

---

# 🌐 API

## Health Check

```http
GET /
```

Example:

```json
{
  "message": "AI Travel Planner Multi Agents API is running."
}
```

## Travel Planning

```http
POST /travel
```

Example request:

```json
{
  "user_query": "Plan a 5-day trip from Bangalore to Calicut"
}
```

Example response structure:

```json
{
  "thread_id": "<thread-id>",
  "flight_results": "...",
  "hotel_results": "..."
}
```

The API will evolve as the remaining agents and human-in-the-loop workflow are implemented.

---

# 🚀 Deployment

The application has been tested in a containerized cloud environment.

Production-oriented architecture:

```text
                    Internet
                       |
                       v
                HTTPS / WAF
                       |
                       v
                Reverse Proxy
                       |
                       v
                 Application
                       |
             ┌─────────┴─────────┐
             |                   |
             v                   v
         Frontend             FastAPI
                                  |
                                  v
                            LangGraph
                                  |
                  ┌───────────────┼───────────────┐
                  |               |               |
                  v               v               v
             Azure OpenAI     Tavily MCP      Secret Store
```

Production considerations:

- HTTPS.
- Authentication and authorization.
- Restricted network access.
- Runtime secret injection.
- Azure Key Vault or approved secret management.
- Container health checks.
- Restart policies.
- Centralized logging.
- Input/output guardrails.
- Human approval for important final decisions.

---

# 🔒 Security

The project follows these principles:

1. Never commit secrets to Git.
2. Never bake production secrets into Docker images.
3. Inject secrets at runtime.
4. Use managed secret storage where appropriate.
5. Do not expose unnecessary ports.
6. Use HTTPS in production.
7. Restrict SSH access.
8. Do not log API keys or credential-bearing URLs.
9. Validate external tool responses.
10. Apply input and output guardrails.
11. Keep a human in the loop before final itinerary approval.

---

# 🧪 Testing

Tests are maintained under:

```text
tests/
```

Run tests with the project's configured test runner.

As the multi-agent workflow grows, testing should cover:

- Agent behavior.
- Graph routing.
- MCP tool integration.
- Input guardrails.
- Output guardrails.
- Structured output validation.
- Human approval/rejection paths.
- API endpoints.
- Error handling.
- End-to-end travel planning.

---

# 📈 Roadmap

### Phase 1 — Foundation

- [x] FastAPI backend
- [x] Streamlit frontend
- [x] LangGraph workflow
- [x] Travel detail extraction
- [x] Flight workflow
- [x] Hotel Agent
- [x] Tavily MCP integration
- [x] Async MCP execution
- [x] Azure OpenAI integration
- [x] Docker
- [x] Docker Compose
- [x] Cloud/EC2 deployment

### Phase 2 — Multi-Agent Expansion

- [ ] Supervisor Agent
- [ ] Travel Research Agent
- [ ] Activity Agent
- [ ] Itinerary Agent
- [ ] Shared agent state
- [ ] Improved structured outputs

### Phase 3 — Safety & Human Control

- [ ] Input Guardrails
- [ ] Output Guardrails
- [ ] Prompt injection protection
- [ ] PII validation
- [ ] Human-in-the-loop approval
- [ ] Re-planning after user feedback

### Phase 4 — Production

- [ ] Azure deployment
- [ ] Azure Key Vault
- [ ] CI/CD
- [ ] Authentication / authorization
- [ ] HTTPS / reverse proxy
- [ ] Observability
- [ ] Agent evaluation
- [ ] Performance and cost optimization

---

# 🎯 What This Project Demonstrates

This project is designed as a practical demonstration of modern **AI Engineering and Agentic AI** concepts:

- Multi-agent architecture.
- Agent orchestration with LangGraph.
- LLM integration with LangChain.
- MCP-based tool integration.
- Asynchronous Python.
- Structured LLM outputs.
- Guardrails.
- Human-in-the-loop AI.
- Docker containerization.
- Docker networking.
- Cloud deployment.
- Runtime secret management.
- API development with FastAPI.
- AI application frontend development with Streamlit.
- Production-oriented security considerations.

---

# 👨‍💻 Project Goal

The long-term goal is to build a production-oriented travel planning platform where specialized AI agents collaborate to research, validate, plan, and continuously refine a travel experience while keeping the **human in control of the final decision**.

```text
Understand
    ↓
Research
    ↓
Recommend
    ↓
Plan
    ↓
Validate
    ↓
Human Review
    ↓
Refine
    ↓
Final Itinerary
```

---

## ⭐ If you find this project useful

Feel free to explore the architecture, experiment with the agents, and extend the workflow with additional tools and travel capabilities.
