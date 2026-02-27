"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


# --- Overview ---
class OverviewResponse(BaseModel):
    total_layoffs: float
    top_country: Optional[str]
    top_industry: Optional[str]
    total_companies: int


# --- Trends ---
class TrendFilters(BaseModel):
    country: Optional[str] = None
    industry: Optional[str] = None
    year: Optional[int] = None


class LayoffsPerMonth(BaseModel):
    month: str
    year: int
    total_laid_off: float
    count: int


class IndustryTrend(BaseModel):
    industry: str
    total_laid_off: float
    count: int


class CountryTrend(BaseModel):
    country: str
    total_laid_off: float
    count: int


class TrendsResponse(BaseModel):
    layoffs_per_month: List[LayoffsPerMonth]
    industry_trends: List[IndustryTrend]
    country_trends: List[CountryTrend]


# --- Companies ---
class CompanySummary(BaseModel):
    company: str
    total_laid_off: float
    funds_raised: Optional[float]
    country: Optional[str]
    industry: Optional[str]


class FundingVsLayoffs(BaseModel):
    company: str
    funds_raised: Optional[float]
    total_laid_off: float


class CompaniesResponse(BaseModel):
    top_companies: List[CompanySummary]
    funding_vs_layoffs: List[FundingVsLayoffs]


# --- Prediction ---
class PredictRequest(BaseModel):
    industry: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    funds_raised: float = Field(..., ge=0)


class PredictResponse(BaseModel):
    risk_level: str


# --- Auth ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str
