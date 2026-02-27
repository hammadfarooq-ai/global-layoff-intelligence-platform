# Backend Documentation

## Stack

- **Framework**: FastAPI
- **Server**: Uvicorn
- **ORM**: SQLAlchemy (sync)
- **Database**: MySQL (PyMySQL)
- **Data**: Pandas (cleaning, EDA)
- **ML**: Scikit-learn, joblib
- **Validation**: Pydantic
- **Auth**: JWT (python-jose), bcrypt (passlib)
- **PDF**: ReportLab

## Folder Structure

```
backend/
├── main.py              # FastAPI app, CORS, lifespan, route mounting
├── database.py          # SQLAlchemy engine, SessionLocal, get_db
├── models.py            # LayoffRecord ORM model
├── schemas.py           # Pydantic request/response schemas
├── data_loader.py       # CSV load, clean, sync to DB, get_cleaned_dataframe
├── requirements.txt
├── routes/
│   ├── overview.py      # /api/overview, /api/overview/filters
│   ├── trends.py        # /api/trends (filters: country, industry, year)
│   ├── companies.py     # /api/companies
│   ├── prediction.py   # POST /api/predict
│   ├── auth.py          # POST /api/auth/login, JWT helpers
│   └── reports.py       # GET /api/reports/pdf, GET /api/reports/eda
├── ml/
│   ├── train.py         # Risk categories, train LR/RF, save joblib
│   └── predictor.py     # Load model, predict_risk(industry, country, funds_raised)
└── data/
    └── layoffs.csv      # Source dataset (or use project data/layoffs.csv)
```

## Database

- **Engine**: MySQL, connection via `mysql+pymysql://...` (configurable with env: `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DATABASE`).
- **Table**: `layoff_records`
  - `id` (PK), `company`, `industry`, `country`, `location`
  - `total_laid_off`, `percentage_laid_off`, `funds_raised`
  - `date`, `year`, `month`, `date_added`
- Tables are created on startup via `create_tables()`; data is synced from CSV with `sync_to_db(replace=True)` (replace truncates and re-inserts).

## Data Cleaning Pipeline (`data_loader.py`)

- Load CSV from `backend/data/layoffs.csv` or `data/layoffs.csv`.
- Normalize column names (lowercase, underscores).
- Coerce numerics: `total_laid_off`, `percentage_laid_off`, `funds_raised`.
- Parse `date` (multiple formats), derive `year` and `month`.
- Fill/leave nulls for optional fields; remove full-row duplicates.
- Persist only selected columns into `layoff_records`.

## ML Module

- **Target**: Risk category from `percentage_laid_off`:
  - **High**: > 50%
  - **Medium**: 20–50%
  - **Low**: < 20%
- **Features**: industry (label‑encoded), country (label‑encoded), funds_raised (numeric).
- **Models**: Logistic Regression and Random Forest; best by cross‑validation accuracy is saved.
- **Artifact**: `backend/ml/layoff_risk_model.joblib` (dict: `model`, `scaler`, `le_industry`, `le_country`, `le_target`).
- **Predictor**: Loads joblib; if file missing, triggers `train_and_save()`. Handles unseen labels by falling back to a default encoding.

## Authentication

- **Login**: `POST /api/auth/login` with `username` and `password`. Demo user: `admin` / `admin123`.
- **Response**: `{ "access_token": "...", "token_type": "bearer" }`.
- **Usage**: Frontend stores token and sends `Authorization: Bearer <token>`.
- **Validation**: `get_current_user` dependency decodes JWT and checks `sub` against a simple in-memory user store (demo only).

## Startup Behavior

1. `lifespan` runs: `create_tables()`, then `sync_to_db(db, replace=True)`.
2. If MySQL is unavailable, sync is skipped and a warning is printed; APIs that need the DB will fail until the DB is up.

For API details, see [API Reference](api.md). For deployment, see [Deployment](deployment.md).
