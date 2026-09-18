from datetime import datetime, timezone
import uuid

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

def generate_id(prefix: str = "TXN") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8].upper()}"

def calculate_risk_level(score: float, low_thresh: float = 40.0, high_thresh: float = 70.0) -> str:
    if score >= high_thresh:
        return "HIGH"
    elif score >= low_thresh:
        return "MEDIUM"
    return "LOW"
