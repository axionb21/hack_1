from fastapi import APIRouter, HTTPException
import numpy as np
from app.schemas.models import PredictRequest, PredictResponse, DriftStatusResponse, LogEntry
from app.core.model_loader import load_model
from app.core.drift_engine import calculate_drift_status
from app.db.crud import insert_prediction, get_recent_logs
from typing import List

router = APIRouter()
model = load_model()

category_map = {"A": 0, "B": 1, "C": 2}
user_map = {"new": 0, "old": 1}
region_map = {"north": 0, "south": 1}

@router.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    cat_val = category_map.get(req.category, 0)
    user_val = user_map.get(req.user_type, 0)
    region_val = region_map.get(req.region, 0)

    X = np.array([[req.amount, cat_val, user_val, region_val]])

    score = model.predict_proba(X)[0][1]
    confidence = abs(score - 0.5) * 2

    timestamp = insert_prediction(
        req.amount, req.category, req.user_type, req.region,
        float(score), float(confidence), req.week
    )

    return {
        "score": float(score),
        "confidence": float(confidence),
        "timestamp": timestamp
    }

@router.get("/drift-status", response_model=DriftStatusResponse)
def get_drift_status():
    return calculate_drift_status()

@router.get("/logs", response_model=List[LogEntry])
def get_logs():
    return get_recent_logs()
