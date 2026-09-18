import pandas as pd
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
