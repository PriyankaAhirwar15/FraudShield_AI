from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.qr import QRScanResponse
from app.services.qr_service import qr_service
from app.core.security import hash_sensitive_identifier
from app.database.models import QRScan

router = APIRouter(prefix="/qr", tags=["QR / Image Scanner"])

@router.post("/scan", response_model=QRScanResponse)
async def scan_qr_endpoint(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image (PNG, JPEG, WebP, etc.)")
        
    try:
        content = await file.read()
        res = qr_service.process_image(content)
        
        # Privacy: Store content hash
        content_hash = hash_sensitive_identifier(res["raw_payload"] or file.filename)
        
        scan_record = QRScan(
            scan_id=res["scan_id"],
            extracted_content_hash=content_hash,
            payload_type=res["payload_type"],
            risk_score=res["qr_risk_score"],
            risk_level=res["risk_level"],
            extracted_details=res["extracted_details"],
            reasons=res["reasons"]
        )
        db.add(scan_record)
        db.commit()
        
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR image processing failed: {str(e)}")
