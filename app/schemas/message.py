from pydantic import BaseModel, Field
from typing import List, Optional

class MessageAnalysisRequest(BaseModel):
    message: str = Field(..., min_length=3, example="Dear customer, your bank account will be blocked today. Update PAN immediately: http://bit.ly/bank-kyc-verify")
    channel: Optional[str] = Field(default="SMS", description="SMS, EMAIL, WHATSAPP")

class MessageAnalysisResponse(BaseModel):
    message_id: str
    phishing_risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    is_phishing: bool
    detected_indicators: List[str]
    extracted_urls: List[str]
    urgency_detected: bool
    threat_detected: bool
    impersonation_detected: bool
    reasons: List[str]
    recommended_action: List[str]
    model_version: str
