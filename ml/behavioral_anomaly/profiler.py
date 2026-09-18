import numpy as np
from datetime import datetime

class UserBehaviorProfile:
    def __init__(
        self,
        user_id: str,
        avg_amount: float = 1500.0,
        std_amount: float = 500.0,
        normal_start_hour: int = 8,
        normal_end_hour: int = 22,
        known_devices: list = None,
        known_beneficiaries: list = None,
        known_locations: list = None
    ):
        self.user_id = user_id
        self.avg_amount = max(avg_amount, 50.0)
        self.std_amount = max(std_amount, 20.0)
        self.normal_start_hour = normal_start_hour
        self.normal_end_hour = normal_end_hour
        self.known_devices = set(known_devices or ["DEV_PRIMARY"])
        self.known_beneficiaries = set(known_beneficiaries or [])
        self.known_locations = set(known_locations or ["Mumbai, IN"])

    def evaluate_behavioral_deviation(
        self,
        amount: float,
        timestamp: datetime,
        device_id: str,
        beneficiary_id: str = None,
        location: str = "Mumbai, IN"
    ) -> dict:
        reasons = []
        scores = []
        
        # 1. Amount deviation
        z_score = (amount - self.avg_amount) / self.std_amount
        ratio = amount / self.avg_amount
        if ratio > 5.0 or z_score > 3.5:
            scores.append(0.9)
            reasons.append(f"Transaction amount (₹{amount:,.2f}) is {ratio:.1f}x above user average (₹{self.avg_amount:,.2f})")
        elif ratio > 2.5 or z_score > 2.0:
            scores.append(0.6)
            reasons.append("Transaction amount significantly exceeds user normal range")
        else:
            scores.append(0.05)
            
        # 2. Time of day
        hour = timestamp.hour if timestamp else 12
        if hour < self.normal_start_hour or hour > self.normal_end_hour:
            scores.append(0.7)
            reasons.append(f"Unusual transaction time ({hour:02d}:00), outside normal active window ({self.normal_start_hour:02d}:00-{self.normal_end_hour:02d}:00)")
        else:
            scores.append(0.0)
            
        # 3. New device
        is_new_device = device_id not in self.known_devices
        if is_new_device:
            scores.append(0.8)
            reasons.append("Transaction initiated from an unrecognized device hardware identifier")
        else:
            scores.append(0.0)
            
        # 4. New beneficiary
        is_new_ben = False
        if beneficiary_id:
            is_new_ben = beneficiary_id not in self.known_beneficiaries
            if is_new_ben:
                scores.append(0.65)
                reasons.append("Beneficiary has no previous transaction history with this account")
            else:
                scores.append(0.0)
                
        # 5. Location change
        is_new_loc = location not in self.known_locations
        if is_new_loc:
            scores.append(0.5)
            reasons.append(f"Geographic location ({location}) differs from primary user activity locations")
            
        raw_anomaly = float(np.clip(np.mean(scores) * 1.5 + (0.35 if (is_new_device and is_new_ben) else 0.0), 0.0, 1.0))
        
        return {
            "behavior_anomaly_score": round(raw_anomaly, 4),
            "is_anomalous": bool(raw_anomaly >= 0.5),
            "is_new_device": is_new_device,
            "is_new_beneficiary": is_new_ben,
            "is_new_location": is_new_loc,
            "amount_z_score": round(float(z_score), 2),
            "amount_ratio": round(float(ratio), 2),
            "reasons": reasons
        }
