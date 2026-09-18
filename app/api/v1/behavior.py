from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.behavior import BehaviorAnalysisRequest, BehaviorAnalysisResponse, UserProfileResponse
from app.services.behavior_service import behavior_service
from app.database.models import User, Device, Beneficiary

router = APIRouter(prefix="/behavior", tags=["Behavioral Anomaly"])

@router.post("/analyze", response_model=BehaviorAnalysisResponse)
def analyze_behavior_endpoint(payload: BehaviorAnalysisRequest, db: Session = Depends(get_db)):
    try:
        res = behavior_service.analyze_behavior(
            db=db,
            user_id=payload.user_id,
            amount=payload.amount,
            device_id=payload.device_id,
            beneficiary_id=payload.beneficiary_id,
            location=payload.location or "Mumbai, IN",
            timestamp=payload.timestamp
        )
        return {
            "user_id": res["user_id"],
            "behavior_anomaly_score": res["behavior_anomaly_score"],
            "is_anomalous": res["is_anomalous"],
            "anomaly_reasons": res["reasons"],
            "profile_metrics": res["profile_metrics"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Behavioral analysis failed: {str(e)}")

@router.get("/profile/{user_id}", response_model=UserProfileResponse)
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User profile not found")
        
    dev_count = db.query(Device).filter(Device.user_id == user_id).count()
    ben_count = db.query(Beneficiary).filter(Beneficiary.user_id == user_id).count()
    
    return {
        "user_id": user.user_id,
        "account_age": user.account_age,
        "avg_transaction_amount": user.avg_transaction_amount,
        "std_transaction_amount": user.std_transaction_amount,
        "normal_start_hour": user.normal_start_hour,
        "normal_end_hour": user.normal_end_hour,
        "known_devices_count": max(dev_count, 1),
        "known_beneficiaries_count": max(ben_count, 0)
    }
