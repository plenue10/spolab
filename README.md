# SPO Lab NBA Insights

This repository contains a FastAPI backend and a Vue 3 frontend that power an NBA data subscription platform. The system enforces role-based access with view limits, tracks dataset uploads, and provides guidance for deployment.

## Backend

- **Framework:** FastAPI
- **Location:** `backend/`
- **Key modules:**
  - `backend/auth/` – registration, login, token-based authentication, and role management.
  - `backend/data/` – dataset upload APIs, view-limit enforcement, and audit trails.
  - `backend/tests/` – pytest suite covering permissions, view quotas, and upload history.

### Running locally

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn main:app --reload
```

### Tests

```bash
cd backend
pytest
```

## Frontend

- **Framework:** Vue 3 with Vite
- **Location:** `frontend/`
- **Features:** Routing for public pages, data browsing, upgrade prompts, and admin tooling placeholders.

```bash
cd frontend
npm install
npm run dev
```

### E2E tests

```bash
cd frontend
npm install
npm run test:e2e
```

## Deployment

- `docker-compose.yml` orchestrates development containers for backend and frontend.
- GitHub Actions workflow (`.github/workflows/ci.yml`) builds the frontend and runs backend tests on every push/PR.

Deployments should follow a staging → production pipeline, leveraging the Docker images produced by each service.
