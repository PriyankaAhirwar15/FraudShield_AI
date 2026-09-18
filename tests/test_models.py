import pytest
import os
from ml.common import load_artifact
from ml.transaction_fraud.features import extract_single_transaction_features
from ml.phishing_url.extractor import extract_url_features, URL_FEATURE_COLUMNS
from ml.qr_scanner.decoder import QRScanner
import pandas as pd

def test_transaction_model_loading_and_inference():
    model_path = "ml/saved_models/transaction_fraud_model.joblib"
    assert os.path.exists(model_path), "Model file missing"
    
    artifact = load_artifact(model_path)
    model = artifact["model"]
    
    feats = extract_single_transaction_features(
        amount=85000.0,
        txn_type="TRANSFER",
        is_new_device=True,
        is_new_beneficiary=True
    )
    probs = model.predict_proba(feats)[0]
    assert len(probs) == 2
    assert 0.0 <= probs[1] <= 1.0

def test_url_model_inference():
    model_path = "ml/saved_models/url_phishing_model.joblib"
    assert os.path.exists(model_path)
    
    artifact = load_artifact(model_path)
    model = artifact["model"]
    
    feats = extract_url_features("http://secure-login-bank-verify.xyz/auth")
    df = pd.DataFrame([feats])[URL_FEATURE_COLUMNS]
    probs = model.predict_proba(df)[0]
    assert len(probs) == 2
    assert probs[1] > 0.5

def test_qr_scanner_payload_parsing():
    scanner = QRScanner()
    res = scanner.parse_payload("upi://pay?pa=scam_mule@upi&pn=RefundDesk&am=15000")
    assert res["qr_detected"] is True
    assert res["payload_type"] == "UPI"
    assert res["qr_risk_score"] >= 40.0
    assert len(res["reasons"]) > 0
