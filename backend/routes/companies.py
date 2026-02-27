"""
Companies API: top 10 by layoffs and funding vs layoffs data.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import LayoffRecord
from schemas import CompaniesResponse, CompanySummary, FundingVsLayoffs

router = APIRouter(prefix="/api/companies", tags=["companies"])


@router.get("", response_model=CompaniesResponse)
def get_companies(db: Session = Depends(get_db)):
    """Return top 10 companies by total layoffs and funding vs layoffs dataset."""
    # Top 10 companies by sum(total_laid_off)
    top_q = (
        db.query(
            LayoffRecord.company,
            func.coalesce(func.sum(LayoffRecord.total_laid_off), 0).label("total_laid_off"),
            func.max(LayoffRecord.funds_raised).label("funds_raised"),
            func.max(LayoffRecord.country).label("country"),
            func.max(LayoffRecord.industry).label("industry"),
        )
        .group_by(LayoffRecord.company)
        .order_by(func.sum(LayoffRecord.total_laid_off).desc())
        .limit(10)
    )
    top_companies = [
        CompanySummary(
            company=r.company,
            total_laid_off=float(r.total_laid_off),
            funds_raised=float(r.funds_raised) if r.funds_raised is not None else None,
            country=r.country,
            industry=r.industry,
        )
        for r in top_q.all()
    ]

    # Funding vs layoffs: one row per company (aggregate)
    fund_q = (
        db.query(
            LayoffRecord.company,
            func.max(LayoffRecord.funds_raised).label("funds_raised"),
            func.coalesce(func.sum(LayoffRecord.total_laid_off), 0).label("total_laid_off"),
        )
        .group_by(LayoffRecord.company)
        .having(func.coalesce(func.sum(LayoffRecord.total_laid_off), 0) > 0)
    )
    funding_vs_layoffs = [
        FundingVsLayoffs(
            company=r.company,
            funds_raised=float(r.funds_raised) if r.funds_raised is not None else None,
            total_laid_off=float(r.total_laid_off),
        )
        for r in fund_q.all()
    ]

    return CompaniesResponse(
        top_companies=top_companies,
        funding_vs_layoffs=funding_vs_layoffs,
    )
