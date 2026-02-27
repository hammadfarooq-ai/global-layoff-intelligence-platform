"""
Global Layoff Intelligence Platform — FastAPI application.
Mounts routes, JWT auth optional on protected endpoints, startup: create tables and sync data.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, get_db
from models import Base
from data_loader import create_tables, sync_to_db, load_and_clean
from routes import overview, trends, companies, prediction, auth, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables and sync CSV data to MySQL on startup."""
    create_tables()
    from sqlalchemy.orm import Session
    from database import SessionLocal
    db = SessionLocal()
    try:
        sync_to_db(db, replace=True)
    except Exception as e:
        # If DB not available (e.g. MySQL not running), skip sync; APIs will fail until DB is up
        print(f"Startup sync warning: {e}")
    finally:
        db.close()
    yield
    # shutdown if needed
    pass


app = FastAPI(
    title="Global Layoff Intelligence Platform",
    description="Analytics and ML APIs for layoff data",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(overview.router)
app.include_router(trends.router)
app.include_router(companies.router)
app.include_router(prediction.router)
app.include_router(auth.router)
app.include_router(reports.router)


@app.get("/")
def root():
    return {"service": "Global Layoff Intelligence Platform", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}
