# Global Layoff Intelligence Platform

A production-style full-stack **data analytics and machine learning dashboard** for layoff data. It provides interactive analytics, filtering, ML-based layoff risk prediction, REST APIs (FastAPI), MySQL storage, and a React frontend.

## Features

- **Advanced data analysis**: Aggregations, trends by month/industry/country, top companies, funding vs layoffs
- **Filtering**: By country, industry, and year across trends and analytics
- **ML prediction**: Layoff risk level (High / Medium / Low) from industry, country, and funds raised (Logistic Regression & Random Forest, best model saved with joblib)
- **REST APIs**: FastAPI with overview, trends, companies, prediction, auth, PDF report, and EDA summary
- **MySQL**: Cleaned layoff data stored and queried via SQLAlchemy
- **React frontend**: Dashboard, Trends, Company Analysis, Risk Prediction pages with Recharts, TailwindCSS, Leaflet map
- **JWT authentication**: Login and protected routes
- **PDF report**: Downloadable analytics report
- **Auto EDA**: Exploratory data summary endpoint

## Tech Stack

| Layer      | Technologies |
|-----------|--------------|
| **Backend** | FastAPI, Uvicorn, Pandas, SQLAlchemy, MySQL (PyMySQL), Scikit-learn, Pydantic, python-jose, ReportLab |
| **Frontend** | React 18, Vite, TailwindCSS, Recharts, Axios, React Router, Leaflet / react-leaflet |

## Project Structure

```
global-layoff-intelligence-platform/
├── backend/          # FastAPI app, DB, ML, routes
├── frontend/         # React (Vite) app
├── data/             # Source layoffs.csv (or backend/data/)
├── docs/             # Markdown documentation
└── README.md
```

## Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- MySQL 8+ (running, with a database created)

### 1. Database

Create a MySQL database (e.g. `layoff_intelligence`) and note credentials.

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

Set environment variables (or use defaults):

- `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`

Place `layoffs.csv` in `backend/data/layoffs.csv` (or keep in project `data/layoffs.csv`; the loader falls back to it).

Run the API:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

On startup, tables are created and CSV data is synced into MySQL.

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

- App: `http://localhost:3000` (or the port Vite prints)
- Default login: **admin** / **admin123**

If the API is on another origin, set `VITE_API_URL`; otherwise the Vite proxy in `vite.config.js` forwards `/api` to `http://localhost:8000`.

## Screenshots

<!-- Add screenshots here, e.g.:
![Dashboard](docs/screenshots/dashboard.png)
![Trends](docs/screenshots/trends.png)
--> 
_Screenshots can be added under this section or in `docs/screenshots/`._

## API Documentation

- **Interactive**: [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger) and [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc) when the backend is running.
- **Markdown reference**: [docs/api.md](docs/api.md) — all endpoints with request/response examples.

## Architecture

High-level flow: **CSV → ETL (clean & load) → MySQL**; **React → FastAPI → MySQL / ML model**.  
Detailed architecture, component diagram, and data flow: **[docs/architecture.md](docs/architecture.md)**.

## Documentation

| Document | Description |
|----------|-------------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/architecture.md](docs/architecture.md) | System overview and diagrams |
| [docs/backend.md](docs/backend.md) | Backend structure, DB, ML, auth |
| [docs/frontend.md](docs/frontend.md) | Frontend structure and pages |
| [docs/api.md](docs/api.md) | API reference |
| [docs/deployment.md](docs/deployment.md) | Env vars, Docker, future improvements |

## Docker

Dockerfile for backend and frontend, plus `docker-compose.yml`, can be used to run the stack in containers. See **[docs/deployment.md](docs/deployment.md)** for environment variables and deployment notes.

## Future Improvements

- Persistent user store and optional refresh tokens
- Enforce JWT on report endpoints if needed
- Scheduled ML retraining and model versioning
- Incremental data sync and paginated data APIs
- Frontend tests, error boundaries, and accessibility
- HTTPS, rate limiting, and structured logging

See **[docs/deployment.md](docs/deployment.md)** for more detail.
