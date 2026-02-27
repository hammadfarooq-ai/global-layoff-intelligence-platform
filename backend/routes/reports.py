"""
Reports API: PDF analytics report download and auto EDA summary.
"""
import io
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from data_loader import get_cleaned_dataframe
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import pandas as pd

router = APIRouter(prefix="/api/reports", tags=["reports"])


def _build_pdf(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="Title", parent=styles["Heading1"], fontSize=18)
    elements = []
    elements.append(Paragraph("Global Layoff Intelligence — Analytics Report", title_style))
    elements.append(Spacer(1, 0.25 * inch))
    elements.append(Paragraph("Overview", styles["Heading2"]))
    elements.append(Paragraph(f"Total records: {len(df)}", styles["Normal"]))
    if "total_laid_off" in df.columns:
        total = df["total_laid_off"].sum()
        elements.append(Paragraph(f"Total layoffs (sum): {total:,.0f}", styles["Normal"]))
    if "company" in df.columns:
        elements.append(Paragraph(f"Unique companies: {df['company'].nunique()}", styles["Normal"]))
    elements.append(Spacer(1, 0.25 * inch))
    elements.append(Paragraph("Top 10 countries by layoffs", styles["Heading2"]))
    if "country" in df.columns and "total_laid_off" in df.columns:
        top_countries = df.groupby("country")["total_laid_off"].sum().nlargest(10).reset_index()
        table_data = [["Country", "Total Laid Off"]] + [
            [str(row[0]), f"{row[1]:,.0f}"] for row in top_countries.itertuples(index=False)
        ]
        t = Table(table_data, colWidths=[2.5 * inch, 2 * inch])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(t)
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("Top 10 industries by layoffs", styles["Heading2"]))
    if "industry" in df.columns and "total_laid_off" in df.columns:
        top_ind = df.groupby("industry")["total_laid_off"].sum().nlargest(10).reset_index()
        table_data = [["Industry", "Total Laid Off"]] + [
            [str(row[0]), f"{row[1]:,.0f}"] for row in top_ind.itertuples(index=False)
        ]
        t2 = Table(table_data, colWidths=[2.5 * inch, 2 * inch])
        t2.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ]))
        elements.append(t2)
    doc.build(elements)
    return buf.getvalue()


@router.get("/pdf")
def download_pdf_report(db: Session = Depends(get_db)):
    """Generate and return PDF analytics report."""
    df = get_cleaned_dataframe(db)
    pdf_bytes = _build_pdf(df)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=layoff_analytics_report.pdf"},
    )


@router.get("/eda")
def get_eda_summary(db: Session = Depends(get_db)):
    """Auto EDA summary: shape, dtypes, missing counts, numeric stats, top categories."""
    df = get_cleaned_dataframe(db)
    summary = {
        "shape": {"rows": int(len(df)), "columns": int(len(df.columns))},
        "columns": list(df.columns),
        "dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
        "missing": df.isnull().sum().astype(int).to_dict(),
        "numeric_stats": {},
        "top_countries": [],
        "top_industries": [],
    }
    for col in ["total_laid_off", "percentage_laid_off", "funds_raised"]:
        if col in df.columns:
            summary["numeric_stats"][col] = {
                "min": float(df[col].min()) if df[col].notna().any() else None,
                "max": float(df[col].max()) if df[col].notna().any() else None,
                "mean": float(df[col].mean()) if df[col].notna().any() else None,
                "median": float(df[col].median()) if df[col].notna().any() else None,
            }
    if "country" in df.columns:
        summary["top_countries"] = (
            df["country"].value_counts().head(15).index.tolist()
        )
    if "industry" in df.columns:
        summary["top_industries"] = (
            df["industry"].value_counts().head(15).index.tolist()
        )
    return summary
