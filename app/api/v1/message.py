from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.message import MessageAnalysisRequest, MessageAnalysisResponse
from app.services.message_service import message_service
from app.core.security import hash_sensitive_identifier
from app.database.models import MessageScan

router = APIRouter(prefix="/message", tags=["Phishing Message Detection"])

@router.post("/analyze", response_model=MessageAnalysisResponse)
def analyze_message_endpoint(payload: MessageAnalysisRequest, db: Session = Depends(get_db)):
    if not payload.message or len(payload.message.strip()) < 3:
        raise HTTPException(status_code=400, detail="Message text is too short or empty")
        
    try:
        res = message_service.analyze_message(payload.message, payload.channel or "SMS")
        
        # Privacy: Store salted hash of text instead of raw sensitive messages
        text_hash = hash_sensitive_identifier(payload.message)
        
        scan_record = MessageScan(
            message_id=res["message_id"],
            message_text_hash=text_hash,
            risk_score=res["phishing_risk_score"],
            risk_level=res["risk_level"],
            detected_indicators=res["detected_indicators"],
            extracted_urls=res["extracted_urls"],
            reasons=res["reasons"]
        )
        db.add(scan_record)
        db.commit()
        
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Message analysis failed: {str(e)}")
