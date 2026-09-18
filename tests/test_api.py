import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "FraudShield" in data["service"]

def test_transaction_fraud_prediction_api():
    payload = {
        "user_id": "USER_1001",
        "amount": 75000.0,
        "transaction_type": "TRANSFER",
        "device_id": "DEV_NEW_881",
        "beneficiary_id": "BEN_NEW_MULE_99",
        "location": "Lagos, NG"
    }
    response = client.post("/api/v1/fraud/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "risk_score" in data
    assert "risk_level" in data
    assert "reasons" in data
    assert len(data["recommended_action"]) > 0

def test_url_scanning_api():
    payload = {"url": "http://secure-login-hdfc-kyc-update.xyz/verify"}
    response = client.post("/api/v1/url/scan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["risk_level"] in ["MEDIUM", "HIGH"]
    assert len(data["detected_indicators"]) > 0

def test_message_analysis_api():
    payload = {
        "message": "Dear customer, your bank account is suspended. Update KYC immediately: http://bit.ly/bank-kyc"
    }
    response = client.post("/api/v1/message/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["urgency_detected"] is True
    assert len(data["extracted_urls"]) == 1

def test_multi_signal_risk_fusion_api():
    payload = {
        "message": "URGENT: Suspicious transaction of Rs 85,000 detected. Click link to reverse: http://cancel-auth.xyz",
        "url": "http://cancel-auth.xyz",
        "transaction": {
            "user_id": "USER_1001",
            "amount": 85000.0,
            "transaction_type": "TRANSFER",
            "device_id": "DEV_NEW_111",
            "beneficiary_id": "BEN_NEW_MULE"
        }
    }
    response = client.post("/api/v1/risk/assess", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["final_risk_score"] >= 70.0
    assert data["multi_stage_scam_chain_detected"] is True
    assert len(data["component_scores"]) >= 2

def test_analytics_and_models_api():
    res_analytics = client.get("/api/v1/analytics/overview")
    assert res_analytics.status_code == 200
    assert "kpi" in res_analytics.json()
    
    res_models = client.get("/api/v1/models/registry")
    assert res_models.status_code == 200
    assert "active_models" in res_models.json()
