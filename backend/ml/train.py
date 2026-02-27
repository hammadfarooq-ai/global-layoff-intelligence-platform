"""
Train layoff risk classifier: High (>50%), Medium (20-50%), Low (<20%).
Uses Logistic Regression and RandomForest; saves best model with joblib.
"""
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Risk categories based on percentage_laid_off
def risk_category(pct: float) -> str:
    if pd.isna(pct):
        return "Medium"  # default for missing
    p = float(pct)
    if p > 0.5:
        return "High"
    if p >= 0.2:
        return "Medium"
    return "Low"


def train_and_save(data_path: str = None, model_dir: str = None):
    """
    Load cleaned data (from CSV or DB), create target, train LR and RF,
    pick best by CV score, save pipeline (encoders + scaler + model) with joblib.
    """
    if data_path is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.path.join(base, "data", "layoffs.csv")
    if not os.path.isfile(data_path):
        alt = os.path.join(os.path.dirname(os.path.dirname(base)), "data", "layoffs.csv")
        if os.path.isfile(alt):
            data_path = alt
    if model_dir is None:
        model_dir = os.path.dirname(os.path.abspath(__file__))

    df = pd.read_csv(data_path)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df["percentage_laid_off"] = pd.to_numeric(df["percentage_laid_off"], errors="coerce")
    df["funds_raised"] = pd.to_numeric(df["funds_raised"], errors="coerce")
    df["industry"] = df["industry"].fillna("Unknown").astype(str)
    df["country"] = df["country"].fillna("Unknown").astype(str)
    df["target"] = df["percentage_laid_off"].apply(risk_category)
    df = df.dropna(subset=["industry", "country"])
    df = df[df["target"].notna()]

    le_industry = LabelEncoder()
    le_country = LabelEncoder()
    X_ind = le_industry.fit_transform(df["industry"].astype(str))
    X_country = le_country.fit_transform(df["country"].astype(str))
    X_funds = df["funds_raised"].fillna(0).values.reshape(-1, 1)
    X = np.hstack([X_ind.reshape(-1, 1), X_country.reshape(-1, 1), X_funds])
    y = df["target"].values

    le_target = LabelEncoder()
    y_enc = le_target.fit_transform(y)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_enc, test_size=0.2, random_state=42, stratify=y_enc
    )

    models = {
        "logistic": LogisticRegression(max_iter=1000, random_state=42),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    }
    best_name = None
    best_score = -1
    for name, clf in models.items():
        scores = cross_val_score(clf, X_train, y_train, cv=3, scoring="accuracy")
        mean_score = scores.mean()
        if mean_score > best_score:
            best_score = mean_score
            best_name = name
    best_model = models[best_name]
    best_model.fit(X_train, y_train)

    pipeline = {
        "model": best_model,
        "scaler": scaler,
        "le_industry": le_industry,
        "le_country": le_country,
        "le_target": le_target,
    }
    path = os.path.join(model_dir, "layoff_risk_model.joblib")
    joblib.dump(pipeline, path)
    return path, best_name, best_score
