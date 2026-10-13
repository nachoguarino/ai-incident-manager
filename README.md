# AI Incident Manager

Backend system for automated software incident analysis.

## Current features

- Incident modeling
- Rule-based incident classification
- Multiple rule matching
- Severity prioritization
- Probable cause detection
- Recommended actions
- Extensible rule engine

## Architecture

...

## Roadmap

- [ ] Automated tests
- [ ] FastAPI API
- [ ] PostgreSQL persistence
- [ ] LLM-powered diagnosis
- [ ] RAG
- [ ] Async processing
- [ ] Docker
- [ ] Observability# AI Incident Manager

A Python backend application for automated software incident analysis, classification, and management.

AI Incident Manager analyzes application incidents using a rule-based engine, identifies probable causes, recommends troubleshooting actions, and stores the results in MongoDB Atlas through a REST API.

## Current Features

- **Incident modeling:** structured representation of software incidents.
- **Rule-based classification:** categorizes incidents using configurable detection rules.
- **Multiple rule matching:** identifies multiple relevant rules for a single incident.
- **Severity prioritization:** determines incident severity based on matched rules.
- **Probable cause detection:** identifies potential causes based on incident information.
- **Recommended actions:** generates troubleshooting recommendations from matching rules.
- **REST API:** exposes incident analysis and retrieval endpoints using FastAPI.
- **MongoDB persistence:** stores incidents and their analysis results in MongoDB Atlas.
- **Incident retrieval:** retrieves individual incidents by ID.
- **Paginated listing:** lists stored incidents with configurable `limit` and `skip` parameters.
- **Input validation and error handling:** handles invalid identifiers, missing incidents, and invalid pagination parameters.
- **Automated tests:** tests the analysis engine, service logic, and API behavior.

## Tech Stack

- **Language:** Python
- **API framework:** FastAPI
- **Database:** MongoDB Atlas
- **Database driver:** PyMongo
- **Testing:** pytest
- **API documentation:** Swagger UI / OpenAPI

## Architecture

The application follows a layered structure that separates incident analysis, business logic, API handling, and database access.

```text
Client
  |
  v
FastAPI (src/api.py)
  |
  v
Incident Service
(src/services/incident_service.py)
  |
  +----> Rule-Based Analyzer
  |      (src/analyzer.py)
  |
  v
Incident Repository
(src/repositories/incident_repository.py)
  |
  v
MongoDB Atlas
```

### Main Components

- **Analyzer:** evaluates incidents against predefined rules and produces classifications, severity levels, probable causes, and recommended actions.
- **Service layer:** coordinates incident processing, invokes the analyzer, and prepares data for persistence and retrieval.
- **API layer:** exposes HTTP endpoints and validates request parameters.
- **Repository layer:** handles database operations.
- **MongoDB Atlas:** persists incident data and analysis results.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns a welcome message. |
| `POST` | `/incidents` | Analyzes an incident and stores the result. |
| `GET` | `/incidents/{incident_id}` | Retrieves an incident by ID. |
| `GET` | `/incidents` | Lists stored incidents with pagination. |

### Pagination

The incident listing endpoint supports:

- `limit`: maximum number of incidents to return (1–100, default: 10).
- `skip`: number of incidents to skip (default: 0).

Example:

```http
GET /incidents?limit=10&skip=0
```

### API Documentation

When the application is running, interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Getting Started

### Prerequisites

- Python
- pip
- A MongoDB Atlas account and database
- A MongoDB connection string configured for the application

### Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
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

Configure the MongoDB connection using the environment variable expected by the application's database configuration. Do not commit credentials or connection strings to the repository.

### Run the API

```bash
python -m uvicorn src.api:app --reload
```

Open `http://127.0.0.1:8000/docs` to explore the API.

### Run Tests

```bash
python -m pytest
```

## Roadmap

- [ ] LLM-powered incident diagnosis
- [ ] Retrieval-Augmented Generation (RAG) for contextual troubleshooting
- [ ] Asynchronous incident processing
- [ ] Docker containerization
- [ ] Observability, structured logging, and metrics
- [ ] Expanded API testing and integration testing
- [ ] Improved filtering and sorting for incident queries

## Project Goals

This project explores backend engineering practices for incident management systems, including API design, layered architecture, database persistence, rule-based analysis, input validation, and automated testing.

Future iterations will investigate how large language models can complement deterministic rules to provide more contextual incident diagnosis and troubleshooting recommendations.

## Status

The core rule-based analyzer, REST API, MongoDB persistence, incident retrieval, paginated listing, and automated tests are implemented.

This project is under active development.
