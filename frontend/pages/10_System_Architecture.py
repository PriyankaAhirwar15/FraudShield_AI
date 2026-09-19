import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

import streamlit as st
from frontend.api_client import health_check

st.title("ℹ️ System Architecture")
st.caption("Technical overview of the FraudShield AI multi-engine fraud detection system")
st.divider()

tab1, tab2, tab3 = st.tabs(["🏗️ Architecture Diagram", "⚙️ Detection Engines", "🔗 API Reference"])

with tab1:
    st.subheader("Multi-Engine Detection Architecture")
    st.markdown("""
```
┌─────────────────────────────────────────────────────────────────┐
│                    FRAUDSHIELD AI PLATFORM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  STREAMLIT FRONTEND (Port 8501)                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Dashboard  │  Transaction  │  URL  │  QR  │  Message    │   │
│  └────────────────────────┬─────────────────────────────────┘   │
│                           │ HTTP/REST                            │
│  FASTAPI BACKEND (Port 8000)                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             API Router (v1)                              │   │
│  │  /fraud  /behavior  /url  /qr  /message  /risk  /alerts │   │
│  └────────┬──────────────────────────────────────┬──────────┘   │
│           │                                      │              │
│  ML SERVICES LAYER                        FUSION SERVICE        │
│  ┌─────────────────────────────┐    ┌────────────────────────┐  │
│  │ FraudService (XGBoost+SHAP) │    │  Multi-Signal Fusion   │  │
│  │ BehaviorService (IsoForest) │───▶│  Weighted Score Blend  │  │
│  │ URLService  (RandomForest)  │    │  Scam Chain Detection  │  │
│  │ MessageService (TF-IDF+LR)  │    └────────────────────────┘  │
│  │ QRService   (OpenCV+Chain)  │                                 │
│  └─────────────────────────────┘                                │
│                    │                                            │
│  DATA LAYER                                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  SQLite / PostgreSQL DB        Joblib Model Artifacts    │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```
    """)
    
    health = health_check()
    if "error" not in health:
        st.success(f"✅ Backend online: v{health.get('version','?')} | DB: {health.get('database_status','?')} | Models: {health.get('models_loaded','?')} loaded")
    else:
        st.warning("⚠️ Backend is offline. Start with: `uvicorn app.main:app --reload`")

with tab2:
    st.subheader("Detection Engine Deep Dive")
    
    with st.expander("💳 Transaction Fraud Engine", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""
**Algorithm:** XGBoost Classifier  
**Features (11):** Amount ratio, velocity, hour-of-day, day-of-week,
is_known_device, is_known_beneficiary, is_high_risk_location,
account_age_days, txn_type_encoded, amount_percentile, is_night_txn

**Why XGBoost?** Handles class imbalance well, natively supports SHAP,
outperforms Random Forest on tabular fraud data in benchmarks.
            """)
        with c2:
            st.markdown("""
**Heuristic Calibration:** Boosts score by +15–30 pts for extreme amount
ratios (>10x), impossible-hour transactions (2-4 AM), and new-device
+ new-beneficiary combinations.

**Explainability:** SHAP TreeExplainer computes per-feature attribution
values on every prediction, surfacing the top-8 risk drivers to the analyst.
            """)
    
    with st.expander("👤 Behavioral Anomaly Engine"):
        st.markdown("""
**Algorithm:** Sklearn Isolation Forest  
**Signals (5):** Amount deviation (z-score), hour-of-day deviation,
is_known_device, is_known_beneficiary, location_deviation

**Baseline:** 30-day rolling window of user activity, rebuilt on each request.
New users trigger elevated baseline deviation penalty.

**Threshold:** Contamination = 0.05 (5% expected anomaly rate).
        """)
    
    with st.expander("🔗 Phishing URL Engine"):
        st.markdown("""
**Algorithm:** Random Forest Classifier  
**Features (17):** URL length, domain length, path depth, subdomain count,
entropy, IP address flag, shortener flag, HTTPS flag, suspicious TLD,
brand keyword in domain, number count in domain, hyphen count,
homoglyph count, query param count, sensitive keyword flag,
known phishing pattern, suspicious path depth.

**Heuristic Boosts:** IP-based URLs +25 pts; URL shorteners +15 pts;
brand+suspicious-TLD combination +30 pts.
        """)
    
    with st.expander("✉️ Message Phishing Engine"):
        st.markdown("""
**Algorithm:** TF-IDF (max_features=8000, ngram 1-2) + Logistic Regression  
**Pattern Detection (5 categories):** Urgency phrases, financial institutions,
threat language, call-to-action keywords, sensitive data requests.

**Calibration:** Pattern-matched score + classifier confidence combined with
weighted blend: 60% ML + 40% pattern signal.
        """)
    
    with st.expander("📷 QR / Image Engine"):
        st.markdown("""
**Technology:** OpenCV QRCodeDetector  
**Payload Types:** UPI, URL, Crypto Address, Plain Text  
**UPI Analysis:** Checks known scam UPI handles, amount pre-fill abuse, impersonation.  
**URL Chaining:** If QR payload is a URL, it is passed to the URL Phishing Engine for secondary analysis.  
**Crypto Detection:** Regex-based Bitcoin/Ethereum/XRP address detection.
        """)
    
    with st.expander("🔀 Multi-Signal Fusion Engine"):
        st.markdown("""
**Method:** Weighted normalized average fusion:

    fused = (w_tx * score_tx + w_beh * score_beh + w_url * score_url
             + w_msg * score_msg + w_qr * score_qr) / sum(active_weights)

**Default Weights:** Transaction=0.35, Behavior=0.25, URL=0.20, Message=0.15, QR=0.05

**Multi-Stage Scam Chain Escalation:**  
If phishing signal (URL or MSG score ≥ 40) AND financial signal (TX or BEH score ≥ 40):  
→ `fused_score = max(fused + 18, 85)` + "MULTI_STAGE_SCAM_CHAIN" critical alert added
        """)

with tab3:
    st.subheader("REST API Reference")
    st.markdown("Base URL: `http://localhost:8000/api/v1`")
    st.markdown("Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)")
    
    endpoints = [
        ("POST", "/fraud/predict", "Transaction fraud scoring with SHAP"),
        ("POST", "/behavior/analyze", "Behavioral anomaly detection"),
        ("GET",  "/behavior/profile/{user_id}", "Retrieve user behavioral profile"),
        ("POST", "/url/scan", "Phishing URL classifier"),
        ("POST", "/message/analyze", "SMS/Email/WhatsApp phishing detection"),
        ("POST", "/qr/scan", "QR code decode + risk assessment (multipart)"),
        ("POST", "/risk/assess", "Multi-signal fusion risk assessment"),
        ("GET",  "/alerts", "Retrieve fraud alerts (paginated)"),
        ("PATCH","/alerts/{alert_id}", "Update alert status"),
        ("GET",  "/analytics/overview", "Analytics KPIs and trend data"),
        ("GET",  "/models/registry", "ML model registry metadata"),
        ("GET",  "/health", "System health check"),
    ]
    
    import pandas as pd
    df = pd.DataFrame(endpoints, columns=["Method", "Endpoint", "Description"])
    
    def color_method(val):
        colors = {"POST": "color:#3498db;font-weight:bold", "GET": "color:#27ae60;font-weight:bold", "PATCH": "color:#f39c12;font-weight:bold"}
        return colors.get(val, "")
    
    st.dataframe(df.style.applymap(color_method, subset=["Method"]), use_container_width=True, height=420)