from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class QRScanResponse(BaseModel):
    scan_id: str
    qr_detected: bool
    payload_type: str = Field(..., example="UPI") # UPI, URL, CRYPTO, TEXT, NONE
    raw_payload: str
    extracted_details: Dict[str, Any] = {}
    qr_risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    is_suspicious: bool
    reasons: List[str]
    recommended_action: List[str]
