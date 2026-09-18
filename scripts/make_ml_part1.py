# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, '.')
from scripts.write_helper import write_f

# ml/common.py
write_f('ml/common.py', '''import os
import json
import joblib
import numpy as np
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, precision_recall_curve, auc,
    confusion_matrix
)
from app.core.logging import logger

def calculate_all_metrics(y_true, y_prob, threshold=0.5):
    y_pred = (np.array(y_prob) >= threshold).astype(int)
    y_t = np.array(y_true).astype(int)
    
    precision = float(precision_score(y_t, y_pred, zero_division=0))
    recall = float(recall_score(y_t, y_pred, zero_division=0))
    f1 = float(f1_score(y_t, y_pred, zero_division=0))
    
    try:
        roc_auc = float(roc_auc_score(y_t, y_prob))
    except Exception:
        roc_auc = 0.5
        
    try:
        precisions, recalls, _ = precision_recall_curve(y_t, y_prob)
        pr_auc = float(auc(recalls, precisions))
    except Exception:
        pr_auc = 0.0
        
    cm = confusion_matrix(y_t, y_pred).tolist()
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "threshold": round(threshold, 3),
        "confusion_matrix": cm
    }

def save_artifact(obj, filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(obj, filepath)
    logger.info(f"Saved artifact to {filepath}")

def load_artifact(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model artifact not found at {filepath}")
    return joblib.load(filepath)

def update_model_registry(registry_path: str, model_data: dict):
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    registry = {"models": {}, "benchmarks": []}
    if os.path.exists(registry_path):
        try:
            with open(registry_path, "r", encoding="utf-8") as f:
                registry = json.load(f)
        except Exception as e:
            logger.warning(f"Could not parse existing registry: {e}")
            registry = {"models": {}, "benchmarks": []}
            
    registry["models"][model_data["model_key"]] = model_data["model_version"]
    
    benchmarks = [b for b in registry.get("benchmarks", []) if b.get("model_name") != model_data.get("model_name")]
    benchmarks.append(model_data)
    registry["benchmarks"] = benchmarks
    
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
    logger.info(f"Updated model registry at {registry_path}")
''')

# ml/transaction_fraud/features.py
write_f('ml/transaction_fraud/features.py', '''import pandas as pd
import numpy as np
from datetime import datetime

TRANSACTION_FEATURE_COLUMNS = [
    "amount",
    "amount_deviation",
    "amount_ratio_to_user_average",
    "transaction_velocity_1h",
    "transaction_velocity_24h",
    "is_night_hour",
    "is_new_device",
    "is_new_beneficiary",
    "account_age_days",
    "is_high_risk_type",
    "location_distance_score"
]

def engineer_transaction_features(df: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame(index=df.index)
    features["amount"] = df["amount"].astype(float)
    
    avg_amt = df.get("historical_avg_amount", 1500.0).astype(float)
    std_amt = df.get("historical_std_amount", 500.0).astype(float).replace(0, 500.0)
    
    features["amount_deviation"] = (features["amount"] - avg_amt) / std_amt
    features["amount_ratio_to_user_average"] = features["amount"] / (avg_amt + 1e-5)
    
    features["transaction_velocity_1h"] = df.get("velocity_1h", 1.0).astype(float)
    features["transaction_velocity_24h"] = df.get("velocity_24h", 2.0).astype(float)
    
    if "hour" in df.columns:
        hours = df["hour"].astype(int)
    elif "timestamp" in df.columns:
        hours = pd.to_datetime(df["timestamp"]).dt.hour
    else:
        hours = 12
    features["is_night_hour"] = ((hours < 6) | (hours >= 23)).astype(int)
    
    features["is_new_device"] = df.get("is_new_device", 0).astype(int)
    features["is_new_beneficiary"] = df.get("is_new_beneficiary", 0).astype(int)
    features["account_age_days"] = df.get("account_age_days", 180).astype(float)
    
    txn_type = df.get("transaction_type", "TRANSFER").astype(str).str.upper()
    features["is_high_risk_type"] = txn_type.isin(["TRANSFER", "CASH_OUT", "CRYPTO"]).astype(int)
    features["location_distance_score"] = df.get("location_distance_score", 0.0).astype(float)
    
    return features[TRANSACTION_FEATURE_COLUMNS]

def extract_single_transaction_features(
    amount: float,
    txn_type: str = "TRANSFER",
    timestamp: datetime = None,
    account_age: int = 180,
    historical_avg: float = 1500.0,
    historical_std: float = 500.0,
    velocity_1h: float = 1.0,
    velocity_24h: float = 2.0,
    is_new_device: bool = False,
    is_new_beneficiary: bool = False,
    location_score: float = 0.0
) -> pd.DataFrame:
    hour = timestamp.hour if timestamp else 14
    is_night = 1 if (hour < 6 or hour >= 23) else 0
    std_safe = historical_std if historical_std > 0 else 500.0
    
    row = {
        "amount": float(amount),
        "amount_deviation": float((amount - historical_avg) / std_safe),
        "amount_ratio_to_user_average": float(amount / max(historical_avg, 1.0)),
        "transaction_velocity_1h": float(velocity_1h),
        "transaction_velocity_24h": float(velocity_24h),
        "is_night_hour": int(is_night),
        "is_new_device": int(is_new_device),
        "is_new_beneficiary": int(is_new_beneficiary),
        "account_age_days": float(account_age),
        "is_high_risk_type": int(txn_type.upper() in ["TRANSFER", "CASH_OUT", "CRYPTO"]),
        "location_distance_score": float(location_score)
    }
    return pd.DataFrame([row])[TRANSACTION_FEATURE_COLUMNS]
''')

# ml/behavioral_anomaly/profiler.py
write_f('ml/behavioral_anomaly/profiler.py', '''import numpy as np
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
''')

# ml/behavioral_anomaly/model.py
write_f('ml/behavioral_anomaly/model.py', '''import numpy as np
from sklearn.ensemble import IsolationForest
from ml.common import save_artifact, load_artifact

class BehavioralIsolationForest:
    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        self.model = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.version = "behavior_iforest_v1"

    def fit(self, X: np.ndarray):
        self.model.fit(X)
        return self

    def score(self, X: np.ndarray) -> np.ndarray:
        raw_scores = self.model.decision_function(X)
        normalized = 1.0 / (1.0 + np.exp(raw_scores * 3.0))
        return np.clip(normalized, 0.0, 1.0)

    def save(self, path: str):
        save_artifact(self, path)

    @classmethod
    def load(cls, path: str):
        return load_artifact(path)
''')

print("make_ml_part1 done.")
