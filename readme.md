# 🌍 World Population REST API

A full-stack Python web application built with **FastAPI** that exposes a RESTful API for querying and managing **world population data** by country and year. The project features a lightweight HTML/JS frontend, PostgreSQL persistence, Google Cloud integrations (BigQuery, Firebase Auth, Firestore, Cloud SQL), and is fully containerised with Docker.

---

## 📖 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Local Setup (without Docker)](#local-setup-without-docker)
  - [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Testing](#testing)
- [Cloud Deployment](#cloud-deployment)

---

## Overview

This project is a RESTful API for world population data. It allows users to browse population statistics by country and year, and provides secured endpoints for creating, updating, and deleting records. Data can be sourced either from a local JSON file or from **Google BigQuery**, and is persisted in a **PostgreSQL** database. The application ships with a simple browser-based frontend for visualising the data.

---

## ✨ Features

- **Paginated queries** — browse all countries, filter by year, or look up a specific country code
- **Full CRUD** — read-only public endpoints + secured write/update/delete endpoints
- **Dual data source** — load data from a local JSON file or Google BigQuery
- **Authentication** — endpoint protection via Google Firebase Auth and API Key validation with Google Firestore
- **Interactive API docs** — auto-generated Swagger UI at `/docs`
- **Containerised** — Docker images for both backend and frontend, orchestrated with Docker Compose
- **GCP-ready** — supports Cloud SQL (Unix socket), BigQuery, Firebase, and Cloud Build CI/CD

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| Database | PostgreSQL (local or GCP Cloud SQL) |
| ORM / Data | SQLAlchemy / raw JSON / BigQuery |
| Auth | Google Firebase Authentication, Firestore API Keys |
| Frontend | Plain HTML + JavaScript (served via FastAPI) |
| Containerisation | Docker, Docker Compose |
| CI/CD | Google Cloud Build (`cloudbuild.yaml`) |

---

## 📁 Project Structure
```
restapi_with_fastapi/
├── backend/                       # FastAPI application
│   ├── main.py                    # App entrypoint & route definitions
│   ├── data_util.py               # Data loading (JSON file or BigQuery)
│   └── ...
├── frontend/                      # Frontend FastAPI app serving HTML
│   └── main.py
├── population_data_jsonline.json  # Sample dataset (fallback data source)
├── back.Dockerfile                # Docker image for the backend
├── front.Dockerfile               # Docker image for the frontend
├── docker-compose.yml             # Multi-container orchestration
├── cloudbuild.yaml                # GCP Cloud Build pipeline
└── readme.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (or Docker)

### Local Setup (without Docker)

**1. Clone the repository**
```bash
git clone https://github.com/lakatostomi/restapi_with_fastapi.git
cd restapi_with_fastapi
```

**2. Set up a virtual environment and install dependencies**
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Run a local PostgreSQL container**
```bash
docker run --name postgres_db \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=population_data \
  -p 5432:5432 \
  postgres:latest -d
```

**4. Create a `.env` file inside the `backend/` folder**
```env
POSTGRES_HOST=localhost:5432
POSTGRES_USER=user
POSTGRES_PASSWORD=mypassword
TABLE_ID=population_data
```

**5. Start the backend**
```bash
uvicorn main:app --port 8008 --reload
```

**6. Start the frontend** (from the `frontend/` directory)
```bash
cd frontend
uvicorn main:app --reload
```

**7. Open your browser**
```
http://localhost:8000/display.html
```

> **Note:** By default the backend loads data from **BigQuery** (which requires a GCP Service Account). To use the local JSON file instead, open `data_util.py`, comment out the BigQuery method, and uncomment the file-based input.

---

### Docker Setup

**1. Build the images**
```bash
docker build -f back.Dockerfile  -t fastapi_backend_app  .
docker build -f front.Dockerfile -t fastapi_frontend_app .
```

**2. Start all services**
```bash
docker-compose --env-file ./backend/.env up
```

**3. Open your browser**
```
http://localhost:8000/display.html
```

---

## ⚙️ Environment Variables

| Variable | Required | Description |
|---|---|---|
| `POSTGRES_HOST` | ✅ | PostgreSQL host and port (e.g. `localhost:5432`) |
| `POSTGRES_USER` | ✅ | Database username |
| `POSTGRES_PASSWORD` | ✅ | Database password |
| `TABLE_ID` | ✅ | Table name in PostgreSQL / dataset ID in BigQuery |
| `PROJECT_ID` | BigQuery only | GCP project ID |
| `DATASET_ID` | BigQuery only | BigQuery dataset ID |
| `GOOGLE_APPLICATION_CREDENTIALS` | BigQuery only | Path to GCP service account JSON key |
| `INSTANCE_UNIX_SOCKET` | Cloud SQL only | Unix socket path for Cloud SQL |
| `FIREBASE_CONFIG` | Firebase only | Path to Firebase config JSON |
| `FIREBASE_AUTH_SA_KEY` | Firebase only | Path to Firebase service account key |

---

## 📡 API Reference

Interactive documentation is available at **`http://127.0.0.1:8000/docs`** (Swagger UI).

### Public Endpoints (GET)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/rest/v1/countries?page=1&size=40` | List all countries (paginated) |
| `GET` | `/api/rest/v1/countries/year/2010?page=1&size=40` | Filter by year |
| `GET` | `/api/rest/v1/countries/code/HUN?page=1&size=40` | Filter by country code |
| `GET` | `/api/rest/v1/countries/save?page=1&size=40` | Fetch from source and persist to DB |

### Secured Endpoints 🔒

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/rest/v1/countries` | Create a new record |
| `PATCH` | `/api/rest/v1/countries/update/{id}` | Update an existing record |
| `DELETE` | `/api/rest/v1/countries/delete/{id}` | Delete a record |
| `POST` | `/api/rest/v1/signup` | Register a new user |
| `POST` | `/api/rest/v1/login` | Log in and receive a token |

---

## 🔐 Authentication

Write endpoints (`POST`, `PATCH`, `DELETE`) are protected by two layers:

- **Google Firebase Authentication** — users must sign up/log in and provide a valid Firebase ID token.
- **API Key Authentication via Google Firestore** — the API validates a key stored in Firestore.

Use `/api/rest/v1/signup` and `/api/rest/v1/login` to register and authenticate before calling secured endpoints.

---

## 🧪 Testing

Run the test suite from within the `backend/` directory:
```bash
pytest test_fastapi.py
```

---

## ☁️ Cloud Deployment

The project includes a `cloudbuild.yaml` for automated builds and deployment via **Google Cloud Build**. For production, it supports:

- **Google Cloud SQL** (via Unix socket connection)
- **Google BigQuery** as the primary data source
- **Google Firebase** for authentication and Firestore-based API key management
- **GCP Secret Manager** for managing environment variables securely

---

## License

This project is open source — feel free to explore, fork, and build on it.
