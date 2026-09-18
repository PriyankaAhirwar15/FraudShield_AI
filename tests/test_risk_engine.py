import pytest
from app.database.session import SessionLocal
from app.services.fusion_service import fusion_service

def test_risk_fusion_low_risk():
    db = SessionLocal()
    try:
        res = fusion_service.assess_multi_signal(
            db=db,
            transaction_data={
                "user_id": "USER_1001",
                "amount": 200.0,
                "transaction_type": "PAYMENT",
                "device_id": "DEV_USER_1001_PRIM",
                "beneficiary_id": "BEN_USER_1001_1",
                "location": "Mumbai, IN"
            }
        )
        assert res["final_risk_score"] < 40.0
        assert res["risk_level"] == "LOW"
        assert res["is_critical_threat"] is False
    finally:
        db.close()

def test_risk_fusion_high_risk_multi_stage_chain():
    db = SessionLocal()
    try:
        res = fusion_service.assess_multi_signal(
            db=db,
            message_text="URGENT: Your bank account will be blocked today. Update KYC: http://bank-kyc.xyz",
            url_text="http://bank-kyc.xyz/verify",
            transaction_data={
                "user_id": "USER_1001",
                "amount": 95000.0,
                "transaction_type": "TRANSFER",
                "device_id": "DEV_UNKNOWN_99",
                "beneficiary_id": "BEN_UNKNOWN_MULE",
                "location": "Lagos, NG"
            }
        )
        assert res["final_risk_score"] >= 70.0
        assert res["risk_level"] == "HIGH"
        assert res["is_critical_threat"] is True
        assert res["multi_stage_scam_chain_detected"] is True
        assert len(res["recommended_actions"]) > 0
    finally:
        db.close()
