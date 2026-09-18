from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.url import URLScanRequest, URLScanResponse
from app.services.url_service import url_service
from app.utils.helpers import generate_id
from app.database.models import URLScan

router = APIRouter(prefix="/url", tags=["Phishing URL Detection"])

@router.post("/scan", response_model=URLScanResponse)
def scan_url_endpoint(payload: URLScanRequest, db: Session = Depends(get_db)):
    if not payload.url or len(payload.url.strip()) < 3:
        raise HTTPException(status_code=400, detail="Invalid or empty URL provided")
        
    try:
        res = url_service.scan_url(payload.url)
        
        # Save scan
        scan_record = URLScan(
            url_id=generate_id("URL"),
            url=res["url"],
            domain=res["domain"],
            risk_score=res["url_risk_score"],
            risk_level=res["risk_level"],
            indicators=res["detected_indicators"],
            reasons=res["reasons"]
        )
        db.add(scan_record)
        db.commit()
        
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL scanning failed: {str(e)}")
