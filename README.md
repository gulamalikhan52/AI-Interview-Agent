AI Interview Agent

An adaptive, AI-powered technical interview platform that conducts personalized interviews, evaluates candidate responses, generates follow-up questions, and provides actionable final feedback.

Live Demo

Application: https://ai-interview-agent-4-mm0t.onrender.com

Overview

AI Interview Agent is a full-stack technical interview system built around a stateful, agentic interview workflow.

Instead of relying on a fixed sequence of questions, the system maintains an interview state and uses candidate information, curriculum context, previous answers, evaluations, and follow-up requirements to determine what happens next.

The application combines:

Streamlit for the interactive frontend

FastAPI for the backend API

LangGraph for stateful interview orchestration

LangChain for LLM integration

Mistral AI for question generation, evaluation, follow-ups, and feedback

JSON-based candidate and curriculum data

Docker for containerized deployment

Key Features

Personalized Technical Interviews

The interview is initialized using candidate-specific information such as:

Candidate ID

Name

Job role

Years of experience

Candidate profile/context

This information is passed into the interview workflow so generated questions can be tailored to the candidate.

Curriculum-Aware Interviewing

The application maintains a structured curriculum containing technical learning topics and associated interview material.

The interview workflow can select a relevant topic/day and generate questions based on the selected lesson.

Dynamic Question Generation

Questions are generated dynamically by the LLM instead of relying entirely on hard-coded questions.

The question-generation service receives candidate and lesson information and creates the current interview question.

Answer Evaluation

Candidate responses are evaluated by the LLM.

The interview state tracks evaluation information such as:

Score

Strengths

Weaknesses

Answer history

Follow-up requirement

Intelligent Follow-Up Questions

If an answer requires deeper evaluation, the system can generate a follow-up question.

This allows the interview to behave more like a real technical interview rather than simply moving to the next question after every response.

Stateful Interview Sessions

Each interview is identified using a sessionId.

The backend maintains state including:

Candidate
Current topic
Current lesson
Current question
Current answer
Evaluation
Question count
Interview history
Follow-up status
Completion status
Final feedback

Final Performance Feedback

Once the interview reaches its configured question limit, the system generates final feedback containing:

Summary

Strengths

Gaps

Next steps

Interactive Streamlit UI

The frontend provides:

Candidate selection

Candidate profile information

Interview start flow

Question display

Answer input

Question counter

Interview progress

Follow-up questions

Final feedback

Error handling

LangGraph Workflow

LangGraph is used to orchestrate the interview workflow and maintain state between different stages of the interview.

Architecture

                         USER
                          |
                          v
              +-----------------------+
              |     Streamlit UI      |
              |                       |
              | Candidate Selection   |
              | Question Display      |
              | Answer Input          |
              | Feedback Display      |
              +-----------+-----------+
                          |
                          | HTTP
                          v
              +-----------------------+
              |      FastAPI API      |
              |                       |
              |  POST /api/interview  |
              +-----------+-----------+
                          |
                          v
              +-----------------------+
              |       LangGraph       |
              |                       |
              | Stateful Workflow     |
              | Routing + State       |
              +-----------+-----------+
                          |
          +---------------+----------------+
          |               |                |
          v               v                v

+----------------+ +-------------+ +-------------------+
| Question | | Answer | | Follow-up |
| Generator | | Evaluator | | Generator |
+--------+-------+ +------+------+ +---------+---------+
| | |
+----------------+------------------+
|
v
+--------------------+
| Mistral AI |
| LLM |
+---------+----------+
|
v
+--------------------+
| Final Feedback |
| Summary |
| Strengths |
| Gaps |
| Next Steps |
+--------------------+

Interview Workflow

                 Candidate Profile
                        |
                        v
                Start Interview
                        |
                        v
                Create Session
                        |
                        v
                  LangGraph
                        |
                        v
              Select Curriculum Topic
                        |
                        v
             Generate Interview Question
                        |
                        v
                Candidate Answers
                        |
                        v
                Evaluate Answer
                        |
             +----------+----------+
             |                     |
             v                     v
       Follow-up Needed?          No
             |                     |
            Yes                    |
             |                     |
             v                     |
       Generate Follow-up          |
             |                     |
             +----------+----------+
                        |
                        v
              Update Interview State
                        |
                        v
              Continue Interview
                        |
                        v
              Question Limit Reached
                        |
                        v
              Generate Final Feedback
                        |
                        v
                Interview Complete

Tech Stack

Backend

Technology

Purpose

Python

Core programming language

FastAPI

REST API backend

Uvicorn

ASGI server

Pydantic

Request/data validation

LangChain

LLM application framework

LangGraph

Stateful workflow orchestration

AI / LLM

Technology

Purpose

Mistral AI

LLM provider

langchain-mistralai

LangChain integration with Mistral

The current interview-generation runtime uses Mistral AI.

Frontend

Technology

Purpose

Streamlit

Interactive web interface

Requests

HTTP communication with FastAPI

Custom CSS

UI styling

Data / Retrieval

Technology

Purpose

JSON

Candidate and curriculum data

FAISS

Vector/retrieval dependency

Development / Deployment

Technology

Purpose

uv

Python dependency and environment management

Docker

Containerization

Docker Compose

Local multi-service orchestration

Git

Version control

GitHub

Source-code hosting

Render

Cloud deployment

Project Structure

AI-Interview-Agent/
│
├── app.py
│
├── data/
│ ├── candidates.json
│ ├── curriculum.json
│ └── technical-spec.md
│
├── frontend/
│ ├── Dockerfile
│ └── streamlit_app.py
│
├── graph/
│ ├── **init**.py
│ ├── graph.py
│ ├── nodes.py
│ ├── router.py
│ └── state.py
│
├── models/
│ └── session.py
│
├── prompts/
│ ├── system.md
│ ├── interviewer.md
│ ├── evaluator.md
│ ├── followup.md
│ └── feedback.md
│
├── retriever/
│ ├── **init**.py
│ ├── candidate.py
│ └── curriculum.py
│
├── schemas/
│ └── interview.py
│
├── services/
│ ├── **init**.py
│ ├── llm.py
│ ├── question_generator.py
│ ├── answer_evaluator.py
│ ├── followup_generator.py
│ └── feedback_generator.py
│
├── tests/
│ ├── **init**.py
│ ├── test_candidate.py
│ ├── test_curriculum.py
│ ├── test_evaluator.py
│ ├── test_feedback.py
│ ├── test_gemini.py
│ ├── test_graph.py
│ └── test_question.py
│
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── PROMPTS.md
├── pyproject.toml
├── uv.lock
└── README.md

Core Components

app.py

The FastAPI application exposes the primary interview endpoint:

POST /api/interview

It:

Creates a new interview session when required.

Validates the incoming request.

Initializes the interview state.

Invokes the LangGraph workflow.

Stores the updated session state.

Evaluates submitted answers.

Generates follow-up questions when required.

Generates final feedback when the interview is complete.

graph/

The graph package contains the interview orchestration layer.

graph.py

Defines the LangGraph workflow.

nodes.py

Contains workflow nodes such as interview question generation and other interview processing steps.

router.py

Handles workflow routing/decision logic.

state.py

Defines the interview state used by the graph.

services/

The service layer separates LLM-related responsibilities.

question_generator.py

Generates technical interview questions.

answer_evaluator.py

Evaluates candidate answers.

followup_generator.py

Generates follow-up questions when deeper probing is required.

feedback_generator.py

Generates final interview feedback.

llm.py

Contains the LLM integration/configuration.

retriever/

Responsible for retrieving candidate and curriculum information used by the interview workflow.

retriever/
├── candidate.py
└── curriculum.py

prompts/

The project keeps prompt responsibilities separated:

prompts/
├── system.md
├── interviewer.md
├── evaluator.md
├── followup.md
└── feedback.md

This makes prompt behavior easier to maintain and modify independently from application logic.

API Documentation

Base Endpoint

/api/interview

Method

POST

Start an Interview

A first request requires a sessionId and candidate information.

Request

{
"sessionId": "abc-123",
"candidate": {
"member": {
"id": "CAND-001",
"name": "John Doe",
"jobRole": "AI Engineer",
"yearsExperience": 2
}
}
}

Response

{
"reply": "Generated interview question...",
"done": false
}

Continue an Interview

The same sessionId is used for subsequent requests.

Request

{
"sessionId": "abc-123",
"message": "My answer to the interview question..."
}

Response

{
"reply": "Next question or follow-up...",
"done": false
}

Completed Interview

When the interview reaches its configured question limit:

{
"reply": "Interview completed.",
"done": true,
"feedback": {
"summary": "...",
"strengths": [],
"gaps": [],
"next": []
}
}

API Home

The backend also exposes:

GET /

Response:

{
"message": "AI Interview Agent Running"
}

Swagger Documentation

When running locally, FastAPI automatically provides interactive API documentation:

http://127.0.0.1:8000/docs

This can be used to test:

POST /api/interview

without using the Streamlit frontend.

Local Development

Prerequisites

Install:

Python 3.13+

Git

uv

Docker Desktop (optional)

Mistral API key

1. Clone the Repository

git clone https://github.com/gulamalikhan52/AI-Interview-Agent.git
cd AI-Interview-Agent

2. Install Dependencies

Using uv:

uv sync

This creates/manages the project's Python environment based on pyproject.toml and uv.lock.

3. Configure Environment Variables

Create a local .env file:

MISTRAL_API_KEY=your_mistral_api_key

If the frontend needs an explicit backend URL:

API_URL=http://127.0.0.1:8000

Never commit .env

The API key must remain outside source control.

Running the Backend

Start FastAPI:

uv run uvicorn app:app --reload

Backend:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

Running the Frontend

Open another terminal:

uv run streamlit run frontend/streamlit_app.py

Streamlit:

http://localhost:8501

Running Both Locally

Use two terminals.

Terminal 1

uv run uvicorn app:app --reload

Terminal 2

uv run streamlit run frontend/streamlit_app.py

Then open:

http://localhost:8501

Docker

The repository contains Docker configuration for containerized execution.

Build

docker compose build

Start

docker compose up

Stop

docker compose down

Environment Variables

Variable

Required

Description

MISTRAL_API_KEY

Yes

API key used to access Mistral AI

API_URL

Deployment-specific

Backend URL used by the Streamlit frontend

Same-container deployment

When Streamlit and FastAPI run inside the same container:

API_URL=http://127.0.0.1:8000

Separate frontend/backend deployment

If frontend and backend are deployed as separate services:

API_URL=https://your-backend-url.example.com

Deployment

The project is containerized using Docker and deployed on Render.

The deployed application uses a combined service architecture where Streamlit and FastAPI run within the same container.

                     Render
                       |
              +--------+--------+
              |                 |
              v                 v
          Streamlit          FastAPI
          $PORT              127.0.0.1:8000
              |                 ^
              |                 |
              +-----------------+
                    API_URL

The Streamlit application communicates with FastAPI through:

http://127.0.0.1:8000

inside the same container.

The LLM API key is configured through Render environment variables.

Testing

The repository contains tests for multiple application components.

Run all tests:

uv run pytest

Run a specific test:

uv run pytest tests/test_graph.py

Other test areas include:

Candidate retrieval
Curriculum retrieval
Answer evaluation
Feedback generation
LLM integration
Graph workflow
Question generation

Design Decisions

Why LangGraph?

The interview is not a single LLM call.

It involves multiple state-dependent operations:

Question
↓
Answer
↓
Evaluation
↓
Follow-up decision
↓
Follow-up OR next question
↓
Completion
↓
Final feedback

LangGraph provides an explicit way to model and orchestrate this stateful workflow.

Why FastAPI?

FastAPI separates the interview engine from the frontend.

The frontend sends interview events to the backend, while the backend owns:

Interview state

LangGraph execution

LLM calls

Evaluation

Follow-up generation

Final feedback

This separation makes the application easier to extend and deploy.

Why Streamlit?

Streamlit provides a Python-first framework for building the interactive interview interface quickly while still allowing custom CSS and UI components.

Why Mistral AI?

Mistral AI is used as the LLM provider for the current interview-generation workflow.

The model is integrated through LangChain's Mistral integration.

Why Session IDs?

An interview is multi-turn.

A sessionId allows the backend to associate multiple requests with the same interview state:

Request 1 → Question 1
Request 2 → Answer 1
Request 3 → Question 2 / Follow-up
Request 4 → Answer 2
...
Request N → Final Feedback

Prompt Architecture

The project separates prompts by responsibility:

prompts/
│
├── system.md
├── interviewer.md
├── evaluator.md
├── followup.md
└── feedback.md

This separation allows individual behaviors to be modified without mixing all instructions into one large prompt.

Security

Important security practices for this project:

Never commit .env.

Never hard-code API keys.

Never expose MISTRAL_API_KEY to the browser.

Store secrets in Render environment variables.

Treat candidate data as sensitive application data.

Use HTTPS in production.

Add authentication before exposing the API to untrusted users.

Add rate limiting before public high-volume usage.

Current Limitations

The current implementation is designed as a project/demo application and has some production limitations.

In-Memory Sessions

Interview sessions are maintained in application memory.

A service restart can therefore remove active session state.

Authentication

The current API does not require user authentication.

Persistent Database

The current implementation does not use a production database for interview sessions and history.

Rate Limiting

Rate limiting and abuse protection are not currently implemented.

Production Observability

Structured logging, metrics, tracing, and monitoring can be expanded for production use.

Future Improvements

Possible improvements include:

PostgreSQL-backed persistent sessions

Redis for session/cache management

Authentication and authorization

Resume upload and parsing

Automatic skill extraction

Difficulty adaptation

Candidate performance analytics

Interview history dashboard

Streaming LLM responses

Rate limiting

Structured logging

Metrics and monitoring

Automated evaluation benchmarks

Multi-model fallback

CI/CD

Production-grade secret management

Persistent candidate profiles

Interview reports and downloadable results

Learning Outcomes

This project demonstrates practical implementation of:

Python backend development

FastAPI

REST APIs

Pydantic

LangChain

LangGraph

LLM integration

Prompt engineering

Stateful agent workflows

Multi-turn conversations

Candidate retrieval

Curriculum retrieval

Answer evaluation

Follow-up generation

Streamlit application development

Docker

Docker Compose

Environment management

Git and GitHub

Cloud deployment

Automated testing

Authors

This project was developed by:

Name

Role

Md Gulam Ali Khan

Developer

Himanshu Yadav

Developer

Jatin Sharma

Developer

Repository

GitHub:https://github.com/gulamalikhan52/AI-Interview-Agent

Live Application:https://ai-interview-agent-4-mm0t.onrender.com

License

This project is currently intended as a project/demo repository.

If you plan to distribute or reuse the project publicly, add an explicit open-source license such as MIT.
