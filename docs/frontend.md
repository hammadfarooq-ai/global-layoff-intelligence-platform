# Frontend Documentation

## Stack

- **Framework**: React 18
- **Build**: Vite
- **Styling**: TailwindCSS
- **Charts**: Recharts
- **Routing**: React Router v6
- **HTTP**: Axios
- **Map**: Leaflet + react-leaflet

## Folder Structure

```
frontend/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── src/
    ├── main.jsx           # React root, BrowserRouter
    ├── App.jsx             # Routes, ProtectedRoute, Layout
    ├── index.css           # Tailwind, fonts (DM Sans, Outfit)
    ├── api/
    │   └── client.js       # Axios instance, getOverview, getTrends, getCompanies, predictRisk, login, getPdfReportUrl, getEdaSummary
    ├── components/
    │   ├── Layout.jsx      # Header, nav links, logout, Outlet
    │   └── KPICard.jsx     # KPI card for dashboard
    └── pages/
        ├── Dashboard.jsx   # Overview KPIs, optional map/charts
        ├── Trends.jsx      # Filters, line/bar charts (Recharts)
        ├── CompanyAnalysis.jsx  # Top companies, funding vs layoffs (e.g. scatter)
        ├── RiskPrediction.jsx   # Form (industry, country, funds_raised), result
        └── Login.jsx       # Login form, token storage, redirect
```

## Pages

| Route | Page | Description |
|-------|------|-------------|
| `/login` | Login | Username/password form; on success stores JWT and redirects to `/`. |
| `/` | Dashboard | Overview KPIs (total layoffs, top country/industry, total companies); optional charts/map. |
| `/trends` | Trends | Filters (country, industry, year); line chart (layoffs per month); bar charts (industry/country trends). |
| `/companies` | Company Analysis | Top 10 companies table; scatter or bar for funding vs layoffs. |
| `/predict` | Risk Prediction | Form: industry, country, funds_raised; submit to `/api/predict`; display risk level. |

## Auth and API

- **Protected routes**: Wrapped in `ProtectedRoute`; redirect to `/login` if no token in `localStorage`.
- **API base URL**: From `Vite` env `VITE_API_URL` or empty (same origin). Vite proxy can forward `/api` to backend (e.g. `http://localhost:8000`).
- **Axios**: `api` instance in `src/api/client.js`; request interceptor adds `Authorization: Bearer <token>` when token exists.

## UI / Theming

- **Fonts**: DM Sans (body), Outfit (headings).
- **Theme**: Dark (e.g. slate-950 background, slate-100 text); accent colors for charts and actions.
- **Components**: Reusable KPI cards; filter dropdowns use options from `/api/overview/filters`.

For API usage and endpoints, see [API Reference](api.md).
