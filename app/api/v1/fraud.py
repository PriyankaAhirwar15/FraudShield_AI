from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.transaction import TransactionInput, TransactionPredictionResponse
from app.services.fraud_service import fraud_service
from app.services.behavior_service import behavior_service
from app.database.models import Transaction

router = APIRouter(prefix="/fraud", tags=["Transaction Fraud"])

@router.post("/predict", response_model=TransactionPredictionResponse)
def predict_fraud(payload: TransactionInput, db: Session = Depends(get_db)):
    try:
        # Behavioral analysis baseline
        beh_res = behavior_service.analyze_behavior(
            db=db,
            user_id=payload.user_id,
            amount=payload.amount,
            device_id=payload.device_id,
            beneficiary_id=payload.beneficiary_id,
            location=payload.location,
            timestamp=payload.timestamp
        )
        
        result = fraud_service.predict_transaction(
            amount=payload.amount,
            transaction_type=payload.transaction_type,
            user_id=payload.user_id,
            transaction_id=payload.transaction_id,
            timestamp=payload.timestamp,
            location=payload.location,
            device_id=payload.device_id,
            beneficiary_id=payload.beneficiary_id,
            account_age=payload.account_age_days or 180,
            historical_avg=beh_res["profile_metrics"]["avg_amount"],
            historical_std=beh_res["profile_metrics"]["std_amount"],
            is_new_device=beh_res["is_new_device"],
            is_new_beneficiary=beh_res["is_new_beneficiary"]
        )
        
        result["behavior_anomaly_score"] = beh_res["behavior_anomaly_score"]
        
        # Save transaction in DB
        tx = Transaction(
            transaction_id=result["transaction_id"],
            user_id=payload.user_id,
            amount=payload.amount,
            transaction_type=payload.transaction_type,
            merchant=payload.merchant,
            location=payload.location,
            device_id=payload.device_id,
            beneficiary_id=payload.beneficiary_id,
            timestamp=payload.timestamp,
            fraud_score=result["fraud_probability"],
            behavior_score=beh_res["behavior_anomaly_score"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            reasons=result["reasons"]
        )
        db.add(tx)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction fraud inference failed: {str(e)}")
