from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class UserProfileResponse(BaseModel):
    user_id: str
    account_age: int
    avg_transaction_amount: float
    std_transaction_amount: float
    normal_start_hour: int
    normal_end_hour: int
    known_devices_count: int
    known_beneficiaries_count: int

class BehaviorAnalysisRequest(BaseModel):
    user_id: str = Field(..., example="USER_1042")
    amount: float = Field(..., gt=0, example=85000.0)
    timestamp: Optional[datetime] = None
    device_id: str = Field(..., example="DEV_NEW_001")
    beneficiary_id: Optional[str] = Field(default=None, example="BEN_UNKNOWN_99")
    location: Optional[str] = Field(default="Mumbai, IN")

class BehaviorAnalysisResponse(BaseModel):
    user_id: str
    behavior_anomaly_score: float
    is_anomalous: bool
    anomaly_reasons: List[str]
    profile_metrics: dict
