import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.database.models import User, Device, Beneficiary
from ml.behavioral_anomaly.profiler import UserBehaviorProfile
from app.core.logging import logger

class BehaviorService:
    def __init__(self):
        # Default fallback profile
        self.default_profile = UserBehaviorProfile("USER_DEFAULT")

    def get_or_create_user_profile(self, db: Session, user_id: str) -> UserBehaviorProfile:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            # Create user baseline
            user = User(
                user_id=user_id,
                account_age=180,
                avg_transaction_amount=1500.0,
                std_transaction_amount=500.0,
                normal_start_hour=8,
                normal_end_hour=22
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        devices = db.query(Device.device_id).filter(Device.user_id == user_id).all()
        known_devices = [d[0] for d in devices] if devices else ["DEV_PRIMARY_" + user_id]
        
        bens = db.query(Beneficiary.beneficiary_id).filter(Beneficiary.user_id == user_id).all()
        known_bens = [b[0] for b in bens]
        
        return UserBehaviorProfile(
            user_id=user_id,
            avg_amount=user.avg_transaction_amount,
            std_amount=user.std_transaction_amount,
            normal_start_hour=user.normal_start_hour,
            normal_end_hour=user.normal_end_hour,
            known_devices=known_devices,
            known_beneficiaries=known_bens,
            known_locations=["Mumbai, IN", "Delhi, IN", "Bengaluru, IN"]
        )

    def analyze_behavior(
        self,
        db: Session,
        user_id: str,
        amount: float,
        device_id: str,
        beneficiary_id: str = None,
        location: str = "Mumbai, IN",
        timestamp: datetime = None
    ) -> dict:
        ts = timestamp or datetime.now()
        profile = self.get_or_create_user_profile(db, user_id)
        
        eval_result = profile.evaluate_behavioral_deviation(
            amount=amount,
            timestamp=ts,
            device_id=device_id,
            beneficiary_id=beneficiary_id,
            location=location
        )
        
        eval_result["user_id"] = user_id
        eval_result["profile_metrics"] = {
            "avg_amount": profile.avg_amount,
            "std_amount": profile.std_amount,
            "normal_hours": f"{profile.normal_start_hour:02d}:00 - {profile.normal_end_hour:02d}:00",
            "known_devices_count": len(profile.known_devices),
            "known_beneficiaries_count": len(profile.known_beneficiaries)
        }
        return eval_result

behavior_service = BehaviorService()
