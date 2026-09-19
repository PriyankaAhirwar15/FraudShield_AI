import os
import requests
from typing import Optional, Dict, Any

_raw_backend = os.getenv("BACKEND_URL", "http://localhost:8000").rstrip("/")
if not _raw_backend.endswith("/api/v1"):
    BASE_URL = f"{_raw_backend}/api/v1"
else:
    BASE_URL = _raw_backend

TIMEOUT = 30

def _get(path: str) -> Dict[str, Any]:
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to FraudShield AI backend at {BASE_URL}. Make sure FastAPI backend is running."}
    except Exception as e:
        return {"error": str(e)}

def _post(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        r = requests.post(f"{BASE_URL}{path}", json=data, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": f"Cannot connect to FraudShield AI backend at {BASE_URL}. Make sure FastAPI backend is running."}
    except Exception as e:
        return {"error": str(e)}

def _post_file(path: str, file_bytes: bytes, filename: str) -> Dict[str, Any]:
    try:
        r = requests.post(
            f"{BASE_URL}{path}",
            files={"file": (filename, file_bytes, "image/png")},
            timeout=TIMEOUT
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to FraudShield AI backend."}
    except Exception as e:
        return {"error": str(e)}

def predict_transaction(payload: Dict) -> Dict:
    return _post("/fraud/predict", payload)

def analyze_behavior(payload: Dict) -> Dict:
    return _post("/behavior/analyze", payload)

def scan_url(url: str) -> Dict:
    return _post("/url/scan", {"url": url})

def analyze_message(message: str, channel: str = "SMS") -> Dict:
    return _post("/message/analyze", {"message": message, "channel": channel})

def scan_qr(image_bytes: bytes, filename: str = "upload.png") -> Dict:
    return _post_file("/qr/scan", image_bytes, filename)

def assess_risk_fusion(payload: Dict) -> Dict:
    return _post("/risk/assess", payload)

def get_alerts(limit: int = 50, status: Optional[str] = None) -> Dict:
    path = f"/alerts?limit={limit}"
    if status:
        path += f"&status={status}"
    return _get(path)

def get_analytics() -> Dict:
    return _get("/analytics/overview")

def get_model_registry() -> Dict:
    return _get("/models/registry")

def health_check() -> Dict:
    return _get("/health")
