from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.risk import MultiSignalAssessmentRequest, MultiSignalAssessmentResponse
from app.services.fusion_service import fusion_service

router = APIRouter(prefix="/risk", tags=["Multi-Signal Risk Fusion Engine"])

@router.post("/assess", response_model=MultiSignalAssessmentResponse)
def assess_risk_fusion(payload: MultiSignalAssessmentRequest, db: Session = Depends(get_db)):
    try:
        tx_dict = payload.transaction.model_dump() if payload.transaction else None
        res = fusion_service.assess_multi_signal(
            db=db,
            transaction_data=tx_dict,
            url_text=payload.url,
            message_text=payload.message,
            qr_payload=payload.qr_payload,
            custom_weights=payload.custom_weights
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Multi-signal risk fusion failed: {str(e)}")
