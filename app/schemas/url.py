from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class URLScanRequest(BaseModel):
    url: str = Field(..., example="http://secure-login-hdfc-kyc-update.com/verify")

class URLScanResponse(BaseModel):
    url: str
    domain: str
    url_risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    is_phishing: bool
    detected_indicators: List[str]
    reasons: List[str]
    domain_characteristics: dict
    recommended_action: List[str]
    model_version: str
