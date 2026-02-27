"""
SQLAlchemy ORM models for the layoff intelligence database.
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.sql import func
from database import Base


class LayoffRecord(Base):
    """Stores cleaned layoff events with company, location, and metrics."""

    __tablename__ = "layoff_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String(255), nullable=False, index=True)
    industry = Column(String(255), nullable=True, index=True)
    country = Column(String(255), nullable=True, index=True)
    location = Column(String(255), nullable=True)
    total_laid_off = Column(Float, nullable=True)
    percentage_laid_off = Column(Float, nullable=True)
    funds_raised = Column(Float, nullable=True)
    date = Column(Date, nullable=True, index=True)
    year = Column(Integer, nullable=True, index=True)
    month = Column(Integer, nullable=True)
    date_added = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<LayoffRecord(company={self.company}, country={self.country}, date={self.date})>"
