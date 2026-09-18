from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from app.schemas.transaction import TransactionInput

class MultiSignalAssessmentRequest(BaseModel):
    session_id: Optional[str] = None
    transaction: Optional[TransactionInput] = None
    url: Optional[str] = None
    message: Optional[str] = None
    qr_payload: Optional[str] = None
    custom_weights: Optional[Dict[str, float]] = None

class ComponentScore(BaseModel):
    name: str
    raw_score: float
    weight: float
    weighted_score: float
    status: str

class MultiSignalAssessmentResponse(BaseModel):
    assessment_id: str
    final_risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    is_critical_threat: bool
    multi_stage_scam_chain_detected: bool
    component_scores: List[ComponentScore]
    summary_reasons: List[str]
    factor_attributions: List[dict]
    recommended_actions: List[str]
    model_versions: Dict[str, str]
