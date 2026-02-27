"""
Prediction API: POST /api/predict returns layoff risk level from ML model.
"""
from fastapi import APIRouter
from schemas import PredictRequest, PredictResponse
from ml.predictor import predict_risk

router = APIRouter(prefix="/api/predict", tags=["prediction"])


@router.post("", response_model=PredictResponse)
def predict(request: PredictRequest):
    """Predict layoff risk level from industry, country, and funds_raised."""
    risk_level = predict_risk(
        industry=request.industry,
        country=request.country,
        funds_raised=request.funds_raised,
    )
    return PredictResponse(risk_level=risk_level)
