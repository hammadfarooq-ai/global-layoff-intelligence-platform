# API Reference

Base URL when running locally: `http://localhost:8000`. Interactive docs: **Swagger UI** at `/docs`, **ReDoc** at `/redoc`.

---

## Overview

### GET /api/overview

Returns dashboard KPIs.

**Response**

```json
{
  "total_layoffs": 1234567.0,
  "top_country": "United States",
  "top_industry": "Consumer",
  "total_companies": 5000
}
```

### GET /api/overview/filters

Returns distinct values for filter dropdowns.

**Response**

```json
{
  "countries": ["Australia", "Brazil", "United States", ...],
  "industries": ["AI", "Consumer", "Finance", ...],
  "years": [2026, 2025, 2024, ...]
}
```

---

## Trends

### GET /api/trends

Returns layoffs per month, industry trends, and country trends. Optional query params filter the data.

**Query parameters**

| Name | Type | Description |
|------|------|-------------|
| `country` | string | Filter by country |
| `industry` | string | Filter by industry |
| `year` | integer | Filter by year |

**Response**

```json
{
  "layoffs_per_month": [
    { "month": "2025-01", "year": 2025, "total_laid_off": 15000.0, "count": 120 }
  ],
  "industry_trends": [
    { "industry": "Consumer", "total_laid_off": 50000.0, "count": 400 }
  ],
  "country_trends": [
    { "country": "United States", "total_laid_off": 80000.0, "count": 600 }
  ]
}
```

---

## Companies

### GET /api/companies

Returns top 10 companies by total layoffs and funding-vs-layoffs dataset.

**Response**

```json
{
  "top_companies": [
    {
      "company": "Amazon",
      "total_laid_off": 16000.0,
      "funds_raised": 8100.0,
      "country": "United States",
      "industry": "Retail"
    }
  ],
  "funding_vs_layoffs": [
    {
      "company": "Company A",
      "funds_raised": 500.0,
      "total_laid_off": 100.0
    }
  ]
}
```

---

## Prediction

### POST /api/predict

Predicts layoff risk level from industry, country, and funds raised.

**Request body**

```json
{
  "industry": "Tech",
  "country": "United States",
  "funds_raised": 500
}
```

**Response**

```json
{
  "risk_level": "High"
}
```

`risk_level` is one of: `"High"`, `"Medium"`, `"Low"`.

---

## Auth

### POST /api/auth/login

Returns a JWT for valid credentials.

**Request body**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response**

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

Use the token in subsequent requests: `Authorization: Bearer <access_token>`.

---

## Reports

### GET /api/reports/pdf

Returns a PDF analytics report (overview stats, top countries, top industries). Response is `application/pdf` with `Content-Disposition: attachment; filename=layoff_analytics_report.pdf`.

### GET /api/reports/eda

Returns an auto EDA summary (shape, dtypes, missing counts, numeric stats, top countries/industries).

**Response (example)**

```json
{
  "shape": { "rows": 4300, "columns": 11 },
  "columns": ["id", "company", "industry", ...],
  "dtypes": { "company": "object", "total_laid_off": "float64", ... },
  "missing": { "company": 0, "total_laid_off": 100, ... },
  "numeric_stats": {
    "total_laid_off": { "min": 1.0, "max": 16000.0, "mean": 250.5, "median": 80.0 },
    "percentage_laid_off": { ... },
    "funds_raised": { ... }
  },
  "top_countries": ["United States", "India", ...],
  "top_industries": ["Consumer", "Retail", ...]
}
```

---

## Health & Root

- **GET /** — Service name and link to docs.
- **GET /health** — `{ "status": "ok" }`.
