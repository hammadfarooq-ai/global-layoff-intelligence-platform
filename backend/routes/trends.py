"""
Trends API: layoffs per month, industry/country trends with optional filters.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import LayoffRecord
from schemas import (
    TrendsResponse,
    LayoffsPerMonth,
    IndustryTrend,
    CountryTrend,
)

router = APIRouter(prefix="/api/trends", tags=["trends"])


def _apply_filters(query, country: str | None, industry: str | None, year: int | None):
    if country:
        query = query.filter(LayoffRecord.country == country)
    if industry:
        query = query.filter(LayoffRecord.industry == industry)
    if year is not None:
        query = query.filter(LayoffRecord.year == year)
    return query


@router.get("", response_model=TrendsResponse)
def get_trends(
    db: Session = Depends(get_db),
    country: str | None = Query(None),
    industry: str | None = Query(None),
    year: int | None = Query(None),
):
    """Return layoffs per month, industry trends, and country trends with optional filters."""
    base = db.query(LayoffRecord)
    base = _apply_filters(base, country, industry, year)

    # Layoffs per month
    month_q = (
        base.with_entities(
            LayoffRecord.month,
            LayoffRecord.year,
            func.coalesce(func.sum(LayoffRecord.total_laid_off), 0).label("total_laid_off"),
            func.count(LayoffRecord.id).label("count"),
        )
        .filter(LayoffRecord.year.isnot(None), LayoffRecord.month.isnot(None))
        .group_by(LayoffRecord.year, LayoffRecord.month)
        .order_by(LayoffRecord.year, LayoffRecord.month)
    )
    months = [
        LayoffsPerMonth(
            month=f"{r.year}-{r.month:02d}",
            year=r.year,
            total_laid_off=float(r.total_laid_off),
            count=r.count,
        )
        for r in month_q.all()
    ]

    # Industry trends (new base query with same filters)
    ind_base = db.query(LayoffRecord)
    ind_base = _apply_filters(ind_base, country, industry, year)
    ind_q = (
        ind_base.with_entities(
            LayoffRecord.industry,
            func.coalesce(func.sum(LayoffRecord.total_laid_off), 0).label("total_laid_off"),
            func.count(LayoffRecord.id).label("count"),
        )
        .filter(LayoffRecord.industry.isnot(None), LayoffRecord.industry != "")
        .group_by(LayoffRecord.industry)
        .order_by(func.sum(LayoffRecord.total_laid_off).desc())
    )
    industry_trends = [
        IndustryTrend(industry=r.industry, total_laid_off=float(r.total_laid_off), count=r.count)
        for r in ind_q.all()
    ]

    # Country trends (new base with same filters)
    c_base = db.query(LayoffRecord)
    c_base = _apply_filters(c_base, country, industry, year)
    country_q = (
        c_base.with_entities(
            LayoffRecord.country,
            func.coalesce(func.sum(LayoffRecord.total_laid_off), 0).label("total_laid_off"),
            func.count(LayoffRecord.id).label("count"),
        )
        .filter(LayoffRecord.country.isnot(None), LayoffRecord.country != "")
        .group_by(LayoffRecord.country)
        .order_by(func.sum(LayoffRecord.total_laid_off).desc())
    )
    country_trends = [
        CountryTrend(country=r.country, total_laid_off=float(r.total_laid_off), count=r.count)
        for r in country_q.all()
    ]

    return TrendsResponse(
        layoffs_per_month=months,
        industry_trends=industry_trends,
        country_trends=country_trends,
    )
