<div align="center">

# 🛡️ FraudShield AI
### **Enterprise Multi-Signal Financial Fraud & Scam Prevention Platform**

*Next-Generation Artificial Intelligence Defense System for Detecting Financial Fraud, Phishing & Social Engineering Threats in Real Time.*

---

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.60+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB5424?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

[Explore Dashboard](#-uiux-interactive-dashboard) • [Architecture](#-system-architecture) • [ML Benchmarks](#-machine-learning-benchmarks) • [API Docs](#-api-endpoints-reference) • [Getting Started](#-quick-start-guide)

---

</div>

## 🌐 Executive Summary

Traditional financial fraud systems analyze transactions in isolation. However, modern cyber financial crimes are **orchestrated, multi-stage social engineering attack chains**:

```
[ 1. Phishing SMS/Email ] ➔ [ 2. Malicious URL ] ➔ [ 3. Fake Portal/QR Code ] ➔ [ 4. High-Risk Transaction ]
```

**FraudShield AI** is an end-to-end multi-engine AI platform designed to evaluate risk signals across **every vector** of the threat lifecycle, combining them through a dynamic **Multi-Signal Fusion Engine** with explainable AI (SHAP) and prescriptive safety actions.

---

## ✨ Key Platform Features

<div align="center">

| Engine | Core Technology | Detection Purpose |
| :--- | :--- | :--- |
| 💳 **Transaction Fraud** | `XGBoost` + `SHAP TreeExplainer` | Anomaly detection on 11 tabular financial features with per-factor risk attribution |
| 👤 **Behavioral Profiler** | `Isolation Forest` (Unsupervised) | Deviations from 30-day user baselines (amounts, night hours, novel devices/beneficiaries) |
| 🔗 **URL Phishing Scanner** | `Random Forest` + Lexical NLP | 17 static lexical features (Shannon entropy, brand impersonation, deceptive subdomains) |
| ✉️ **Message Analyzer** | `TF-IDF` + `Logistic Regression` | Social engineering NLP for urgency, threat language, authority impersonation, and OTP traps |
| 📷 **QR / Image Scanner** | `OpenCV QRCodeDetector` | Payload classification (UPI deep-links, phishing URLs, crypto addresses) + scanner chaining |
| 🔀 **Multi-Signal Fusion** | Weighted Adaptive Ensemble | Cross-vector score fusion with **Multi-Stage Scam Chain Escalation** ($\ge 85$ Critical) |

</div>

---

## 🏗️ System Architecture

```
                                  ┌────────────────────────────────────────────────────────┐
                                  │             FRAUDSHIELD AI ECOSYSTEM                   │
                                  └────────────────────────────────────────────────────────┘
                                                              │
                    ┌─────────────────────────────────────────┴─────────────────────────────────────────┐
                    ▼                                                                                   ▼
   ┌─────────────────────────────────┐                                                 ┌─────────────────────────────────┐
   │    STREAMLIT FRONTEND (8501)    │                                                 │     FASTAPI BACKEND (8000)      │
   │  ┌───────────────────────────┐  │                                                 │  ┌───────────────────────────┐  │
   │  │ 📊 Executive Dashboard    │  │                   REST JSON API                 │  │ ⚡ High-Performance Router │  │
   │  │ 💳 Transaction Scanner    │  │ ═══════════════════════════════════════════════▶│  │ 🛡️ Pydantic v2 Validation │  │
   │  │ 🔗 URL Phishing Scanner   │  │                     Requests                    │  │ 💾 SQLAlchemy ORM Session │  │
   │  │ 📷 QR / Image Scanner     │  │                                                 │  └─────────────┬─────────────┘  │
   │  │ ✉️ Message NLP Analyzer   │  │◀═══════════════════════════════════════════════│                │                 │
   │  │ 👤 Behavioral Profiler    │  │                 JSON Responses                  │                ▼                 │
   │  │ 🚨 Fraud Alerts Console   │  │                                                 │  ┌───────────────────────────┐  │
   │  │ 📈 Deep Pattern Analytics │  │                                                 │  │   ML INFERENCE SERVICES   │  │
   │  │ 🔬 Model Benchmarks       │  │                                                 │  │ • FraudService (XGBoost)  │  │
   │  │ 🔀 Multi-Signal Fusion    │  │                                                 │  │ • BehaviorService (IForest)│ │
   │  │ ℹ️ System Architecture    │  │                                                 │  │ • URLService (RandForest) │  │
   │  └───────────────────────────┘  │                                                 │  │ • MessageService (TF-IDF) │  │
   └─────────────────────────────────┘                                                 │  │ • QRService (OpenCV)      │  │
                                                                                       │  └─────────────┬─────────────┘  │
                                                                                       │                │                 │
                                                                                       │                ▼                 │
                                                                                       │  ┌───────────────────────────┐  │
                                                                                       │  │   MULTI-SIGNAL FUSION     │  │
                                                                                       │  │  Normalized Weight Matrix │  │
                                                                                       │  │  + Scam Chain Escalator   │  │
                                                                                       │  └───────────────────────────┘  │
                                                                                       └─────────────────────────────────┘
```

---

## 🔬 Machine Learning Benchmarks

> ℹ️ *Note: Evaluated across held-out synthetic test partitions.*

### 📊 Supervised Transaction Fraud Model Comparison

```
                      Precision    Recall    F1-Score    ROC-AUC
Logistic Regression    97.22%     100.00%     98.59%      1.0000
Random Forest         100.00%      98.57%     99.28%      1.0000
XGBoost (CHAMPION)    100.00%     100.00%    100.00%      1.0000  ⭐⭐⭐⭐⭐
```

### ⚡ Production Model Summary

| Model Task | Champion Algorithm | F1-Score | ROC-AUC | Training Dataset Size |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction Fraud** | `XGBoost Classifier` | **1.0000** | **1.0000** | 8,000 transactions |
| **Behavioral Anomaly** | `Isolation Forest` | **0.9077** | **0.9510** | 10,000 profiles (Unsupervised) |
| **Phishing URL Detection** | `Random Forest` | **1.0000** | **1.0000** | 3,200 domain/URLs |
| **Message Phishing NLP** | `TF-IDF + Logistic Regression` | **1.0000** | **1.0000** | 2,400 messages |

---

## 🎨 UI/UX Interactive Dashboard

FraudShield AI features a custom **Dark Cybersecurity UI Theme** (`#0a0e1a` glassmorphism backdrop with neon blue & emerald accents):

<div align="center">

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  🛡️ FraudShield AI — Security Operations Console                                      │
├────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                        │
│  [ 📊 Total Txns: 1,450 ]  [ ⚠️ Flagged: 84 ]  [ 🚨 High Risk: 38 ]  [ 💰 Saved: ₹4.8M ]│
│                                                                                        │
│  ┌──────────────────────────────────────┐  ┌────────────────────────────────────────┐  │
│  │ 📈 8-Day Threat Velocity Timeline    │  │ 🍩 Risk Level Distribution             │  │
│  │    /\__/\_                           │  │     [HIGH: 28%  MED: 32%  LOW: 40%]    │  │
│  └──────────────────────────────────────┘  └────────────────────────────────────────┘  │
│                                                                                        │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │ 🔍 Live Transaction & SHAP Factor Attribution Waterfall                          │  │
│  │    [amount_ratio]           ████████████████ (+2.45) ⬆ Increases Risk             │  │
│  │    [is_night_txn]           ████████ (+1.12)         ⬆ Increases Risk             │  │
│  │    [is_known_device]        ████ (-0.85)             ⬇ Reduces Risk               │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

</div>

### 📑 11 Dedicated Application Modules:
- **📊 01 Executive Dashboard** — Real-time KPIs, threat timelines, donut distribution, and geographic activity charts.
- **💳 02 Transaction Scanner** — Interactive transaction testing with instant SHAP attribution waterfalls.
- **🔗 03 URL Scanner** — Safe static lexical analysis of suspicious links without visiting malicious hosts.
- **📷 04 QR / Image Scanner** — QR upload & live QR code generator with UPI, crypto address, and URL chaining.
- **✉️ 05 Message Analyzer** — NLP analysis for SMS/Email/WhatsApp scam patterns and urgency triggers.
- **👤 06 Behavioral Profiler** — Deviations tester evaluating activity against historical user baselines.
- **🚨 07 Fraud Alerts** — Full alert triage management console with status filters (`NEW`, `INVESTIGATION`, `RESOLVED`).
- **📈 08 Deep Analytics** — Hourly heatmaps, attack channel breakdowns, and automated AI insight callouts.
- **🔬 09 Model Performance** — Active model registry, benchmark tables, and F1 / ROC-AUC visualizations.
- **ℹ️ 10 System Architecture** — Technical system breakdown, engine mechanics, and REST API directory.
- **🔀 11 Risk Fusion** — Interactive multi-vector risk simulator demonstrating scam-chain escalations.

---

## 🚀 Quick Start Guide

### 📋 Prerequisites
- **Python 3.10+**
- **Git**

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PriyankaAhirwar15/FraudShield_AI.git
cd FraudShield_AI
```

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Setup Environment & Train Models
```bash
# Copy example environment configuration
copy .env.example .env

# Generate synthetic data & train champion ML models
python scripts/generate_synthetic_data.py
python scripts/train_models.py
python scripts/seed_database.py
```

### 4️⃣ Run FastAPI Backend
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
📖 *Interactive OpenAPI Documentation available at:* [http://localhost:8000/docs](http://localhost:8000/docs)

### 5️⃣ Launch Streamlit Frontend
In a new terminal:
```bash
streamlit run frontend/app.py
```
🌐 *Web Dashboard available at:* [http://localhost:8501](http://localhost:8501)

### 6️⃣ Run Automated Test Suite
```bash
pytest -v
```
✅ *All 14 unit and integration tests passing.*

---

## 🐳 Docker Deployment

Run the entire platform (Backend + Frontend) with a single command:

```bash
docker-compose up --build
```

- **Backend API**: `http://localhost:8000`
- **Frontend Dashboard**: `http://localhost:8501`

---

## 📡 API Endpoints Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | System health check and model loading status |
| `POST` | `/fraud/predict` | Transaction fraud inference with SHAP factor attribution |
| `POST` | `/behavior/analyze` | User behavioral anomaly evaluation |
| `GET` | `/behavior/profile/{user_id}` | Retrieve historical user behavioral baseline |
| `POST` | `/url/scan` | Phishing URL lexical classifier |
| `POST` | `/message/analyze` | SMS/Email/WhatsApp social engineering NLP scanner |
| `POST` | `/qr/scan` | QR image upload decoding and payload risk analysis |
| `POST` | `/risk/assess` | Multi-signal fusion assessment with scam chain logic |
| `GET` | `/alerts` | Retrieve paginated fraud alerts |
| `PATCH` | `/alerts/{alert_id}` | Update alert triage status |
| `GET` | `/analytics/overview` | Executive KPI and aggregated risk analytics |
| `GET` | `/models/registry` | Active ML models and benchmark metrics |

---

## 📁 Repository Structure

```
FraudShield_AI/
├── app/                        # FastAPI Backend Application
│   ├── api/v1/                 # 11 REST API Endpoint Routers
│   ├── core/                   # Security, Masking & Structured Logging
│   ├── database/               # SQLAlchemy ORM Models & DB Session
│   ├── schemas/                # Pydantic v2 Request/Response Models
│   ├── services/               # 7 Domain Business Logic Services
│   ├── config.py               # Pydantic BaseSettings Configuration
│   └── main.py                 # FastAPI Application Entrypoint
├── ml/                         # Machine Learning Core
│   ├── transaction_fraud/      # Feature Engineering (11 features)
│   ├── behavioral_anomaly/     # Profiler & Isolation Forest
│   ├── phishing_url/           # 17-feature Lexical URL Extractor
│   ├── phishing_message/       # NLP Preprocessor & Pattern Matcher
│   ├── qr_scanner/             # OpenCV QR Decoder & Scanner Chain
│   ├── explainability/         # SHAP TreeExplainer Wrapper
│   └── saved_models/           # Model Artifacts & Registry
├── frontend/                   # Streamlit Multi-Page Dashboard
│   ├── pages/                  # 11 Interactive Streamlit Pages
│   ├── components/             # Reusable UI Cards, Gauges & Charts
│   ├── api_client.py           # Typed HTTP Backend Client
│   └── app.py                  # Entry Point & Theme Stylesheet
├── data/synthetic/             # Templated Training Datasets
├── docker/                     # Backend & Frontend Dockerfiles
├── scripts/                    # Generation, Training & Seeding Scripts
├── tests/                      # 14 Pytest Unit & Integration Tests
├── docker-compose.yml          # Multi-Container Compose Config
├── requirements.txt            # Python Dependencies
├── LICENSE                     # MIT License
└── README.md                   # Platform Documentation
```

---

## 👩‍💻 Author & Credits

<div align="center">

### **Built with ❤️ by Priyanka Ahirwar**

[![GitHub](https://img.shields.io/badge/GitHub-PriyankaAhirwar15-181717?style=for-the-badge&logo=github)](https://github.com/PriyankaAhirwar15)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com)

*Designed and developed as an industry-standard End-to-End AI/ML Security Engineering Project.*

</div>

---

## ⚠️ Disclaimer

> **IMPORTANT NOTICE**: **FraudShield AI** is an advanced artificial intelligence demonstration and decision-support platform built for research, educational, and security portfolio purposes. Risk scores and classifications generated by the models represent probabilistic risk estimates and should **not** replace certified banking fraud protocols, official anti-money laundering (AML) compliance investigations, or primary human judgment. The author and contributors are not liable for decisions made based on outputs from this system.
