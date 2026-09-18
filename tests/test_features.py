import pytest
import pandas as pd
from datetime import datetime

from ml.transaction_fraud.features import extract_single_transaction_features, TRANSACTION_FEATURE_COLUMNS
from ml.phishing_url.extractor import extract_url_features, detect_url_indicators
from ml.phishing_message.preprocessor import clean_text, extract_urls_from_text, analyze_message_patterns

def test_transaction_feature_extraction():
    feats = extract_single_transaction_features(
        amount=50000.0,
        txn_type="TRANSFER",
        timestamp=datetime(2026, 9, 18, 2, 30),
        account_age=180,
        historical_avg=1500.0,
        historical_std=500.0,
        velocity_1h=4.0,
        velocity_24h=8.0,
        is_new_device=True,
        is_new_beneficiary=True,
        location_score=0.85
    )
    
    assert len(feats) == 1
    assert set(feats.columns) == set(TRANSACTION_FEATURE_COLUMNS)
    assert feats["amount"].iloc[0] == 50000.0
    assert feats["amount_ratio_to_user_average"].iloc[0] > 30.0
    assert feats["is_night_hour"].iloc[0] == 1
    assert feats["is_new_device"].iloc[0] == 1
    assert feats["is_new_beneficiary"].iloc[0] == 1
    assert feats["is_high_risk_type"].iloc[0] == 1

def test_url_feature_extraction():
    phish_url = "http://secure-login-hdfc-kyc.update.account.verify.xyz/auth/login"
    feats = extract_url_features(phish_url)
    indicators = detect_url_indicators(phish_url, feats)
    
    assert feats["is_https"] == 0
    assert feats["suspicious_tld"] == 1
    assert feats["suspicious_keyword_count"] >= 3
    assert feats["num_subdomains"] >= 3
    assert len(indicators) > 0

def test_message_feature_extraction():
    msg = "URGENT: Your bank account is blocked today due to pending KYC. Click http://bit.ly/bank-verify to update PAN immediately."
    cleaned = clean_text(msg)
    urls = extract_urls_from_text(msg)
    analysis = analyze_message_patterns(msg)
    
    assert "urgent" in cleaned
    assert len(urls) == 1
    assert analysis["urgency_detected"] is True
    assert analysis["credential_harvesting_detected"] is True
    assert len(analysis["detected_indicators"]) >= 2
