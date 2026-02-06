from pydantic import BaseModel
from typing import List, Optional

class PredictRequest(BaseModel):
    amount: float
    category: str
    user_type: str
    region: str
    week: int

class PredictResponse(BaseModel):
    score: float
    confidence: float
    timestamp: str

class DriftStatusResponse(BaseModel):
    overall_score: float
    status: str
    input_drift: float
    output_drift: float
    confidence_drift: float
    subgroup: Optional[str] = None
    alerts: List[str] = []

class LogEntry(BaseModel):
    id: int
    timestamp: str
    score: float
    confidence: float
    week: int
