from pydantic import BaseModel
from typing import List, Dict, Any

class KPISummary(BaseModel):
    total_transactions: int
    suspicious_transactions: int
    high_risk_events: int
    fraud_alerts: int
    avg_risk_score: float
    estimated_prevented_loss: float

class AnalyticsOverview(BaseModel):
    kpi: KPISummary
    fraud_trends_timeline: List[Dict[str, Any]]
    fraud_by_transaction_type: Dict[str, int]
    fraud_by_hour: Dict[int, int]
    fraud_by_location: Dict[str, int]
    risk_distribution: Dict[str, int]
    scam_channel_breakdown: Dict[str, int]
