"""
Load trained layoff risk model and predict risk level from industry, country, funds_raised.
"""
import os
import joblib
import numpy as np

_MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "layoff_risk_model.joblib")
_pipeline = None


def _get_pipeline():
    global _pipeline
    if _pipeline is None:
        if not os.path.isfile(_MODEL_PATH):
            from ml.train import train_and_save
            train_and_save()
        _pipeline = joblib.load(_MODEL_PATH)
    return _pipeline


def predict_risk(industry: str, country: str, funds_raised: float) -> str:
    """
    Predict layoff risk level: High, Medium, or Low.
    Uses saved model; if industry/country unseen, falls back to encoding or default.
    """
    pipe = _get_pipeline()
    le_ind = pipe["le_industry"]
    le_country = pipe["le_country"]
    scaler = pipe["scaler"]
    model = pipe["model"]
    le_target = pipe["le_target"]

    industry = (industry or "Unknown").strip()
    country = (country or "Unknown").strip()
    funds = float(funds_raised) if funds_raised is not None else 0.0

    try:
        ind_enc = le_ind.transform([industry])[0]
    except ValueError:
        ind_enc = 0
    try:
        country_enc = le_country.transform([country])[0]
    except ValueError:
        country_enc = 0

    X = np.array([[ind_enc, country_enc, funds]], dtype=float)
    X_scaled = scaler.transform(X)
    pred_enc = model.predict(X_scaled)[0]
    return le_target.inverse_transform([pred_enc])[0]
