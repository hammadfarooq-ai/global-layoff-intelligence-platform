"""
Overview API: aggregate KPIs (total layoffs, top country/industry, total companies) and filter options.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import LayoffRecord
from schemas import OverviewResponse

router = APIRouter(prefix="/api/overview", tags=["overview"])


@router.get("/filters")
def get_filters(db: Session = Depends(get_db)):
    """Return distinct countries, industries, and years for filter dropdowns."""
    countries = [
        r[0] for r in
        db.query(LayoffRecord.country).filter(
            LayoffRecord.country.isnot(None), LayoffRecord.country != ""
        ).distinct().order_by(LayoffRecord.country).all()
    ]
    industries = [
        r[0] for r in
        db.query(LayoffRecord.industry).filter(
            LayoffRecord.industry.isnot(None), LayoffRecord.industry != ""
        ).distinct().order_by(LayoffRecord.industry).all()
    ]
    years = [
        r[0] for r in
        db.query(LayoffRecord.year).filter(LayoffRecord.year.isnot(None)).distinct().order_by(LayoffRecord.year.desc()).all()
    ]
    return {"countries": countries, "industries": industries, "years": years}


@router.get("", response_model=OverviewResponse)
def get_overview(db: Session = Depends(get_db)):
    """Return dashboard overview: total layoffs, top country, top industry, total companies."""
    total_layoffs = (
        db.query(func.coalesce(func.sum(LayoffRecord.total_laid_off), 0)).scalar() or 0
    )
    total_companies = db.query(func.count(func.distinct(LayoffRecord.company))).scalar() or 0

    top_country_row = (
        db.query(LayoffRecord.country, func.sum(LayoffRecord.total_laid_off).label("tot"))
        .filter(LayoffRecord.country.isnot(None), LayoffRecord.country != "")
        .group_by(LayoffRecord.country)
        .order_by(func.sum(LayoffRecord.total_laid_off).desc())
        .first()
    )
    top_industry_row = (
        db.query(LayoffRecord.industry, func.sum(LayoffRecord.total_laid_off).label("tot"))
        .filter(LayoffRecord.industry.isnot(None), LayoffRecord.industry != "")
        .group_by(LayoffRecord.industry)
        .order_by(func.sum(LayoffRecord.total_laid_off).desc())
        .first()
    )

    return OverviewResponse(
        total_layoffs=float(total_layoffs),
        top_country=top_country_row[0] if top_country_row else None,
        top_industry=top_industry_row[0] if top_industry_row else None,
        total_companies=int(total_companies),
    )
