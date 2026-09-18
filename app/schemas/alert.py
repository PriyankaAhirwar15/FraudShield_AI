from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AlertUpdate(BaseModel):
    status: str = Field(..., example="RESOLVED_BLOCKED") # NEW, UNDER_INVESTIGATION, RESOLVED_BLOCKED, RESOLVED_FALSE_POSITIVE

class FraudAlertResponse(BaseModel):
    alert_id: str
    event_type: str
    event_id: str
    risk_score: float
    risk_level: str
    reasons: List[str]
    recommended_action: List[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
