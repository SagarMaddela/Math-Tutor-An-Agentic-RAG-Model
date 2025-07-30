# Math Routing Agent: Agentic RAG for Step-by-Step Math Tutoring

## Overview

**Math Routing Agent** is an Agentic-RAG (Retrieval-Augmented Generation) system designed to replicate a **mathematics professor**. It provides **step-by-step math solutions** by intelligently routing queries through:

* A **VectorDB-backed Knowledge Base**
* A **Web Search pipeline with MCP**
* A **Human-in-the-Loop (HITL)** feedback system for continual learning

The agent ensures **safe, accurate, and explainable math tutoring** for students. This project is built using **FastAPI** for backend and **React** for frontend, with agent orchestration handled by **LangGraph** and optional feedback tuning via **DSPy**.

---

## Key Features

* **Input/Output Guardrails** via AI Gateway for privacy and content control
* **Agentic Routing** between KB, Web Search, and MCP
* **Mathematics-focused Knowledge Base**
* **MCP-based Web Search** for unfamiliar or complex queries
* **Feedback Learning** through Human-in-the-Loop validation
* \[Bonus] **JEE Bench Evaluation** support for benchmarking

---

## Architecture

```mermaid
graph TD
    A[User Query] --> B[AI Gateway (Input Guardrails)]
    B --> C{Knowledge Base Match?}
    C -- Yes --> D[VectorDB (Qdrant/Weaviate)]
    D --> E[LangGraph Agent]
    C -- No --> F[MCP Web Search Pipeline]
    F --> E
    E --> G[Response Generator]
    G --> H[Evaluation Agent (DSPy Optional)]
    H --> I[User Feedback]
    I --> J[Refinement + Logging]
    J --> K[AI Gateway (Output Guardrails)]
    K --> L[Final Answer]
```

---

## Tech Stack

| Component            | Tool / Library            |
| -------------------- | ------------------------- |
| Backend              | FastAPI, LangGraph        |
| Frontend             | React                     |
| Knowledge Base       | Qdrant / Weaviate         |
| Web Search           | Tavily / Exa / Serper     |
| Agent Framework      | LangGraph, DSPy (Bonus)   |
| Guardrails           | AI Gateway, PII Filtering |
| Feedback Evaluation  | DSPy / Custom Review UI   |
| Benchmarking Dataset | JEE Bench (Optional)      |

---

## Project Structure

```
math-routing-agent/
├── backend/
│   ├── main.py
│   ├── agents/
│   ├── knowledge_base/
│   ├── mcp_pipeline/
│   ├── feedback/
│   ├── guardrails/
│   └── utils/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
├── jee_benchmark/
│   ├── run_benchmark.py
├── docs/
│   └── final_proposal.pdf
├── README.md
└── requirements.txt
```

---

## Key Capabilities

### Guardrails (AI Gateway)

* **Input Filtering**: Blocks non-educational or inappropriate queries
* **Output Validation**: Ensures explanations remain factual and age-appropriate

### Knowledge Base

* **Vector Search** using `Qdrant` or `Weaviate`
* Loaded with questions from `Khan Academy`, `JEE Math`, or `OpenAI Math Dataset`
* Sample KB Queries:

  * *“Find the derivative of x² + 3x + 1”*
  * *“What is the area of a triangle with base 5 and height 4?”*

### Web Search + MCP

* If query not in KB, routes to `Tavily/Serper` with **MCP Protocol** wrapping context
* Sample Search Queries:

  * *“What is the value of log(10^3)?”*
  * *“Explain Lagrange Multipliers in simple terms”*

### Feedback Learning (HITL)

* Student reviews solution
* If unsatisfactory, feedback routed to Evaluation Agent
* Agent updates knowledge and flags ambiguous queries for human review

---

## Bonus: JEE Benchmark Evaluation

* Benchmark run on **JEE Bench** dataset
* Metrics: Accuracy, Step-Correctness, Clarity, Response Time
* Results available in `/jee_benchmark/report.csv`

---

## Getting Started

### Install Backend Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run FastAPI Backend

```bash
uvicorn main:app --reload
```

### Run Frontend React App

```bash
cd frontend
npm install
npm start
```

---

## Example API Call

**POST** `/solve`

```json
{
  "question": "Find the integration of sin(x) dx"
}
```

**Response:**

```json
{
  "source": "knowledge_base",
  "steps": [
    "We know ∫sin(x) dx = -cos(x) + C",
    "Therefore, the final answer is -cos(x) + C"
  ],
  "feedback_prompt": "Was this explanation clear?"
}
```



---

## Final Proposal

Find detailed documentation including:

* Guardrail Strategy
* KB & Web Routing Pipeline
* HITL Agent Flow
* MCP Strategy
* Sample Use Cases

📄 Located at: `/docs/final_proposal.pdf`

---

## Contributing

Contributions welcome! Please fork the repo and create a pull request with proposed changes.

---

## License

MIT License - see `LICENSE` for details.

---


