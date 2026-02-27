# Deployment

## Environment Variables (Backend)

| Variable | Default | Description |
|----------|---------|-------------|
| `MYSQL_USER` | `root` | MySQL username |
| `MYSQL_PASSWORD` | `root` | MySQL password |
| `MYSQL_HOST` | `localhost` | MySQL host |
| `MYSQL_PORT` | `3306` | MySQL port |
| `MYSQL_DATABASE` | `layoff_intelligence` | Database name |
| `JWT_SECRET` | (dev default) | Secret for JWT signing; **must** be overridden in production |

## Running Locally (without Docker)

1. **MySQL**: Create database `layoff_intelligence` (or as per `MYSQL_*`).
2. **Backend**: From `backend/`, install deps (`pip install -r requirements.txt`), then run `uvicorn main:app --reload --host 0.0.0.0 --port 8000`. Ensure `backend/data/layoffs.csv` exists (or `data/layoffs.csv` at project root).
3. **Frontend**: From `frontend/`, run `npm install` and `npm run dev`. Set `VITE_API_URL` if the API is on another origin; otherwise use Vite proxy to `/api` → `http://localhost:8000`.

## Docker

- **Backend**: `Dockerfile` in `backend/` (Python, install deps, run Uvicorn).
- **Frontend**: `Dockerfile` in `frontend/` (Node build, serve static with nginx or similar).
- **Orchestration**: `docker-compose.yml` at project root defines services (e.g. `backend`, `frontend`, `mysql`). Backend depends on MySQL; frontend can proxy to backend.

See root [README.md](../README.md) for exact `docker-compose` service names and commands.

## Future Improvements

- **Auth**: Replace in-memory user store with DB-backed users and optional refresh tokens.
- **API security**: Enforce JWT on sensitive routes (e.g. PDF, EDA) if required.
- **ML**: Retrain pipeline on schedule; version models; add more features (e.g. date, company size).
- **Data**: Incremental CSV sync; validation and logging; optional data API with pagination.
- **Frontend**: Unit/e2e tests; error boundaries; loading states; accessibility.
- **Ops**: HTTPS, rate limiting, structured logging, health checks for DB and ML load.
