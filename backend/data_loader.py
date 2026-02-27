"""
Data cleaning pipeline: load CSV, clean, and optionally sync to MySQL.
Handles missing values, dates, year/month extraction, and duplicates.
"""
import os
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from models import LayoffRecord, Base
from database import engine

# Resolve path: prefer backend/data/layoffs.csv, fallback to project data/layoffs.csv
_BASE = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH = os.path.join(_BASE, "data", "layoffs.csv")
if not os.path.isfile(_DATA_PATH):
    _DATA_PATH = os.path.join(os.path.dirname(_BASE), "data", "layoffs.csv")


def _parse_date(val):
    """Parse various date formats to date object."""
    if pd.isna(val) or val == "":
        return None
    if isinstance(val, datetime):
        return val.date()
    s = str(val).strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def load_and_clean() -> pd.DataFrame:
    """
    Load layoffs CSV and apply cleaning pipeline:
    - Handle missing values (fill/coerce numeric, keep nullable where appropriate)
    - Convert date to datetime, extract year and month
    - Remove duplicates
    """
    df = pd.read_csv(_DATA_PATH)
    # Normalize column names (strip, lowercase for internal use)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Ensure required columns exist (map common variants)
    col_map = {
        "total_laid_off": "total_laid_off",
        "percentage_laid_off": "percentage_laid_off",
        "funds_raised": "funds_raised",
        "date": "date",
        "company": "company",
        "industry": "industry",
        "country": "country",
        "location": "location",
    }
    for standard, possible in [
        ("total_laid_off", ["total_laid_off"]),
        ("percentage_laid_off", ["percentage_laid_off"]),
        ("funds_raised", ["funds_raised"]),
        ("date", ["date"]),
        ("company", ["company"]),
        ("industry", ["industry"]),
        ("country", ["country"]),
        ("location", ["location"]),
    ]:
        if standard not in df.columns and possible:
            for p in possible:
                if p in df.columns:
                    df = df.rename(columns={p: standard})
                    break

    # Numeric: coerce to float, leave NaN where missing
    for col in ["total_laid_off", "percentage_laid_off", "funds_raised"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Date parsing and year/month
    if "date" in df.columns:
        df["date_parsed"] = df["date"].apply(_parse_date)
        df["date"] = df["date_parsed"]
        df["year"] = df["date"].apply(lambda x: x.year if x else None)
        df["month"] = df["date"].apply(lambda x: x.month if x else None)
        df = df.drop(columns=["date_parsed"], errors="ignore")

    # String columns: fill empty with None
    for col in ["company", "industry", "country", "location"]:
        if col in df.columns:
            df[col] = df[col].astype(object).where(df[col].notna(), None)
            df[col] = df[col].astype(str).replace("nan", "").replace("", None)

    # Remove duplicates (full row)
    df = df.drop_duplicates()

    # Select columns we persist
    out_cols = [
        "company", "industry", "country", "location",
        "total_laid_off", "percentage_laid_off", "funds_raised",
        "date", "year", "month",
    ]
    out_cols = [c for c in out_cols if c in df.columns]
    return df[out_cols].copy()


def create_tables():
    """Create all tables defined in Base."""
    Base.metadata.create_all(bind=engine)


def sync_to_db(db: Session, replace: bool = True) -> int:
    """
    Sync cleaned DataFrame to MySQL. If replace=True, truncate and insert.
    Returns number of rows inserted.
    """
    df = load_and_clean()
    if replace:
        LayoffRecord.__table__.drop(engine, checkfirst=True)
        LayoffRecord.__table__.create(engine)

    count = 0
    for _, row in df.iterrows():
        rec = LayoffRecord(
            company=row.get("company") or "",
            industry=row.get("industry"),
            country=row.get("country"),
            location=row.get("location"),
            total_laid_off=row.get("total_laid_off"),
            percentage_laid_off=row.get("percentage_laid_off"),
            funds_raised=row.get("funds_raised"),
            date=row.get("date"),
            year=int(row["year"]) if pd.notna(row.get("year")) else None,
            month=int(row["month"]) if pd.notna(row.get("month")) else None,
        )
        db.add(rec)
        count += 1
    db.commit()
    return count


def get_cleaned_dataframe(db: Session) -> pd.DataFrame:
    """Return full cleaned dataset as DataFrame from DB (for EDA, reports)."""
    from sqlalchemy import text
    with engine.connect() as conn:
        return pd.read_sql(text("SELECT * FROM layoff_records"), conn)
