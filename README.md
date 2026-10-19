# AI Incident Manager

A Python backend application that analyzes software incidents using a hybrid approach combining deterministic rules and Large Language Models (LLMs).

AI Incident Manager classifies incidents, estimates severity, identifies probable causes, recommends troubleshooting actions, and stores analysis results in MongoDB Atlas. It provides a REST API built with FastAPI and a web dashboard for submitting and reviewing incidents.

## Features

- **Hybrid incident analysis:** combines a rule-based engine with OpenAI-powered analysis.
- **Rule-based classification:** identifies known incident patterns using configurable detection rules.
- **Multiple rule matching:** detects multiple relevant patterns in a single incident.
- **Severity prioritization:** combines rule-based and LLM severity assessments, prioritizing the highest severity.
- **Probable cause analysis:** generates potential explanations for reported incidents.
- **Recommended actions:** provides troubleshooting suggestions based on rules and LLM analysis.
- **Fallback handling:** returns rule-based results when LLM analysis fails.
- **REST API:** exposes endpoints for incident creation, retrieval, and listing.
- **MongoDB persistence:** stores incidents and analysis results in MongoDB Atlas.
- **Web dashboard:** provides a user interface for submitting incidents and reviewing their analysis.
- **Input validation and error handling:** handles invalid identifiers, missing incidents, and invalid pagination parameters.
- **Automated tests:** validates analyzer behavior, service logic, database repository operations, and API endpoints.

## Tech Stack

- **Language:** Python
- **API framework:** FastAPI
- **LLM integration:** OpenAI API
- **Database:** MongoDB Atlas
- **Database driver:** PyMongo
- **Frontend:** HTML, CSS, JavaScript
- **Testing:** pytest, HTTPX
- **API documentation:** Swagger UI / OpenAPI

## Architecture

The application follows a layered architecture that separates HTTP handling, business logic, incident analysis, and database access.

```text
                    User
                     |
                     v
              Web Dashboard
                     |
                     v
               FastAPI API
                (src/api.py)
                     |
                     v
              Incident Service
                     |
                     v
             Hybrid Analyzer
                     |
              +------+------+
              |             |
              v             v
       Rule-Based Engine   OpenAI LLM
              |             |
              +------+------+
                     |
                     v
            Combined Analysis
                     |
                     v
           Incident Repository
                     |
                     v
               MongoDB Atlas
```

### Main Components

- **API layer:** exposes HTTP endpoints and serves the dashboard.
- **Service layer:** coordinates incident processing, analysis, and persistence.
- **Rule-based analyzer:** evaluates incidents against predefined detection rules.
- **LLM analyzer:** generates contextual incident classifications, probable causes, and troubleshooting recommendations.
- **Hybrid analyzer:** combines rule-based and LLM results, prioritizes severity, and falls back to rule-based analysis if the LLM fails.
- **Repository layer:** handles database operations.
- **MongoDB Atlas:** persists incident records and their analysis results.
- **Frontend dashboard:** allows users to submit incidents and inspect their results.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web dashboard. |
| `POST` | `/incidents` | Analyzes and stores a new incident. |
| `GET` | `/incidents` | Lists incidents with pagination. |
| `GET` | `/incidents/{incident_id}` | Retrieves a specific incident by ID. |

### Pagination

The incident listing endpoint supports the following query parameters:

- `limit`: maximum number of incidents to return (1–100, default: 10).
- `skip`: number of incidents to skip (default: 0).

Example:

```http
GET /incidents?limit=10&skip=0
```

### API Documentation

When the application is running, interactive API documentation is available at:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Getting Started

### Prerequisites

- Python 3.12 or a compatible Python version.
- pip
- A MongoDB Atlas database.
- An OpenAI API key.

### Installation

Clone the repository:

```bash
git clone <https://github.com/nachoguarino/ai-incident-manager>
cd ai-incident-manager
```

Create and activate a virtual environment.

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root directory:

```env
MONGODB_URI=your_mongodb_connection_string
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder values with your own credentials.

**Security:** Never commit your `.env` file or expose API keys and database credentials in source code.

### Run the Application

Start the development server:

```bash
python -m uvicorn src.api:app --reload
```

Open the following URL to access the dashboard:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

Explore the API through Swagger UI:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Run Tests

Execute the automated test suite:

```bash
python -m pytest
```

## Roadmap

- [ ] Improve incident severity assessment using explicit impact criteria.
- [ ] Add structured output validation for LLM responses.
- [ ] Distinguish rule-based findings from LLM-generated hypotheses in the dashboard.
- [ ] Add configurable timeouts and retry policies for LLM requests.
- [ ] Add Docker support for easier deployment.
- [ ] Improve observability with structured logs and operational metrics.
- [ ] Explore Retrieval-Augmented Generation (RAG) for contextual troubleshooting.

## Project Goals

This project explores practical backend engineering concepts through an incident management use case, including REST API design, layered architecture, database persistence, deterministic rule engines, LLM integration, error handling, and automated testing.

The goal is to demonstrate how traditional backend logic and LLMs can work together to support software incident investigation.

## Status

The core application is implemented, including the hybrid analysis engine, FastAPI endpoints, MongoDB persistence, web dashboard, and automated tests.

The project is currently focused on improving reliability, documentation, and deployment readiness.
