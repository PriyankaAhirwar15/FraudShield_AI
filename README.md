# FraudShield AI

> Enterprise Multi-Signal Financial Fraud and Scam Prevention Platform
> A production-style AI/ML portfolio project demonstrating end-to-end fraud detection across transaction, behavioral, URL, QR, and messaging threat vectors.

## Overview

FraudShield AI goes beyond basic transaction fraud detection. Modern financial scams operate in multiple coordinated stages:

```
Phishing SMS -> Malicious URL -> Fake Payment Page -> Malicious QR -> Transaction
```

FraudShield AI detects threats at every stage and fuses the signals into a unified risk score with full explainability.

---

## Key Features

- 5 Independent Detection Engines (Transaction, Behavioral, URL, Message, QR)
- Multi-Stage Scam Chain Detection (escalation rule when phishing + financial signals co-occur)
- SHAP Explainability on every transaction prediction
- Prescriptive Recommended Actions per risk event
- FastAPI REST backend with OpenAPI docs (http://localhost:8000/docs)
- 11-page Streamlit dashboard with dark cybersecurity theme
- SQLite by default (PostgreSQL-ready via DATABASE_URL env var)
- 14/14 automated tests passing

---

## Architecture

```
STREAMLIT FRONTEND (Port 8501)
  Pages: Dashboard | Transaction | URL | QR | Message | Alerts | Analytics | Models | Fusion | Architecture
                       |
                  HTTP/REST
                       |
FASTAPI BACKEND (Port 8000)
  /api/v1/fraud  /behavior  /url  /qr  /message  /risk  /alerts  /analytics  /models  /health
                       |
  ML SERVICES LAYER                    FUSION SERVICE
  FraudService  (XGBoost + SHAP)       Multi-Signal Weighted Fusion
  BehaviorService (Isolation Forest)   Scam Chain Escalation Logic
  URLService    (Random Forest)
  MessageService (TF-IDF + LogReg)
  QRService     (OpenCV + URL Chain)
                       |
             SQLite / PostgreSQL DB
             Joblib Model Artifacts (ml/saved_models/)
```

---

## Detection Engines

### 1. Transaction Fraud Engine
- Algorithm: XGBoost Classifier (champion from 3-model benchmark)
- Features (11): amount_ratio, transaction_velocity, hour_of_day, day_of_week, is_known_device, is_known_beneficiary, is_high_risk_location, account_age_days, txn_type_encoded, amount_percentile, is_night_txn
- Explainability: SHAP TreeExplainer with per-feature attribution values
- Heuristic Calibration: +15-30 point boosts for extreme amount ratios, night + new-device combinations

### 2. Behavioral Anomaly Engine
- Algorithm: Isolation Forest (unsupervised)
- Signals: Amount z-score, hour-of-day deviation, device novelty, beneficiary novelty, location deviation
- Baseline: 30-day rolling window per user, rebuilt on each inference call

### 3. Phishing URL Engine
- Algorithm: Random Forest Classifier
- Features (17): URL/domain length, path depth, subdomain count, Shannon entropy, IP flag, shortener flag, HTTPS, suspicious TLD, brand-in-domain, digit/hyphen/homoglyph counts, query params, sensitive keywords

### 4. Message Phishing Engine
- Algorithm: TF-IDF (8,000 features, 1-2 ngrams) + Logistic Regression
- Pattern Categories: Urgency, financial impersonation, threats, call-to-action, sensitive data requests
- Score: 60% ML + 40% pattern signal blend

### 5. QR / Image Scanning Engine
- Technology: OpenCV QRCodeDetector
- Payload Types: UPI payments, URLs, crypto addresses, plain text
- URL Chaining: QR-embedded URLs fed to Phishing URL Engine for secondary analysis

### 6. Multi-Signal Fusion Engine
```
fused_score = sum(weight_i * score_i) / sum(active_weights)

Scam Chain Rule:
  if (url_score >= 40 OR msg_score >= 40) AND (tx_score >= 40 OR beh_score >= 40):
      fused_score = max(fused_score + 18, 85)
      alert: MULTI_STAGE_SCAM_CHAIN
```
Default Weights: Transaction=0.35, Behavior=0.25, URL=0.20, Message=0.15, QR=0.05

---

## ML Model Benchmark

IMPORTANT: All metrics measured on synthetic, templated test data. Real-world scores will be substantially lower.

### Transaction Fraud -- 3-Model Comparison

| Model                   | Precision | Recall | F1 Score | ROC-AUC |
|-------------------------|-----------|--------|----------|---------|
| Logistic Regression     | 0.9722    | 1.0000 | 0.9859   | 1.0000  |
| Random Forest           | 1.0000    | 0.9857 | 0.9928   | 1.0000  |
| XGBoost (CHAMPION)      | 1.0000    | 1.0000 | 1.0000   | 1.0000  |

### All Production Models

| Model                        | Algorithm            | F1 Score | ROC-AUC | Train Samples |
|------------------------------|----------------------|----------|---------|---------------|
| Transaction Fraud            | XGBoost              | 1.0000   | 1.0000  | 8,000         |
| Behavioral Anomaly           | Isolation Forest     | 0.9077   | 0.9510  | 10,000        |
| Phishing URL                 | Random Forest        | 1.0000   | 1.0000  | 3,200         |
| Message Phishing             | TF-IDF + LogReg      | 1.0000   | 1.0000  | 2,400         |

The Behavioral Anomaly model scores lower because it is unsupervised -- it has no ground-truth labels during training, making evaluation harder and more realistic.

---

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/FraudShield_AI.git
cd FraudShield_AI
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
copy .env.example .env
# Defaults work out of the box
```

### 3. Generate Data and Train Models

```bash
python scripts/generate_synthetic_data.py
python scripts/train_models.py
python scripts/seed_database.py
```

### 4. Start the Backend

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
# Interactive docs -> http://localhost:8000/docs
```

### 5. Start the Frontend

```bash
# In a second terminal:
streamlit run frontend/app.py
# Dashboard -> http://localhost:8501
```

### 6. Run Tests

```bash
pytest -v
# Expected: 14 passed
```

---

## Docker Setup

```bash
docker-compose up --build
# Backend  -> http://localhost:8000
# Frontend -> http://localhost:8501
```

---

## API Reference

Base URL: http://localhost:8000/api/v1

| Method | Endpoint                        | Description                                  |
|--------|---------------------------------|----------------------------------------------|
| POST   | /fraud/predict                  | Transaction fraud scoring + SHAP explanation |
| POST   | /behavior/analyze               | Behavioral anomaly detection                 |
| GET    | /behavior/profile/{user_id}     | User behavioral profile                      |
| POST   | /url/scan                       | Phishing URL classification                  |
| POST   | /message/analyze                | SMS/Email/WhatsApp phishing detection        |
| POST   | /qr/scan                        | QR decode + risk assessment (multipart)      |
| POST   | /risk/assess                    | Multi-signal fusion risk assessment          |
| GET    | /alerts                         | Retrieve fraud alerts (paginated)            |
| PATCH  | /alerts/{alert_id}              | Update alert status                          |
| GET    | /analytics/overview             | KPIs and trend data                          |
| GET    | /models/registry                | ML model registry + benchmark metrics        |
| GET    | /health                         | System health check                          |

### Example: Transaction Fraud Prediction

```bash
curl -X POST http://localhost:8000/api/v1/fraud/predict \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"USER_001\",
    \"amount\": 85000,
    \"transaction_type\": \"TRANSFER\",
    \"device_id\": \"DEV_UNKNOWN_99\",
    \"beneficiary_id\": \"BEN_UNKNOWN_44\",
    \"location\": \"Lagos, NG\",
    \"account_age_days\": 90,
    \"historical_avg_amount\": 1200,
    \"timestamp\": \"2024-01-15T02:30:00\"
  }"
```

---

## Project Structure

```
FraudShield_AI/
|-- app/                    FastAPI backend
|   |-- api/v1/             11 REST endpoint routers
|   |-- core/               Logging, security utilities
|   |-- database/           SQLAlchemy models and session
|   |-- schemas/            Pydantic v2 request/response schemas
|   |-- services/           Business logic (7 services)
|   |-- config.py           Pydantic settings
|   `-- main.py             FastAPI app entry point
|
|-- ml/                     Machine learning components
|   |-- transaction_fraud/  Feature engineering
|   |-- behavioral_anomaly/ Profiler + IsolationForest wrapper
|   |-- phishing_url/       URL feature extractor
|   |-- phishing_message/   NLP preprocessor
|   |-- qr_scanner/         OpenCV QR decoder
|   |-- explainability/     SHAP explainer wrapper
|   |-- saved_models/       Serialized model artifacts (.joblib)
|   `-- common.py           Metrics, artifact I/O, registry
|
|-- frontend/               Streamlit multi-page dashboard
|   |-- pages/              11 page modules
|   |-- components/         kpi_card, charts, explanations
|   |-- api_client.py       HTTP client for FastAPI
|   `-- app.py              Entry point with global CSS theme
|
|-- data/synthetic/         Generated training datasets
|-- scripts/                Data generation, training, seeding
|-- tests/                  14-test pytest suite
|-- docker/                 Dockerfiles
|-- docker-compose.yml
`-- requirements.txt
```

---

## Streamlit Frontend Pages

| Page | Module |
|------|--------|
| Executive Dashboard   | KPI cards, trend timeline, risk distribution |
| Transaction Scanner   | ML form + SHAP waterfall chart |
| URL Phishing Scanner  | URL input + indicator breakdown |
| QR / Image Scanner    | Upload or generate QR for live scan |
| Message Analyzer      | Paste SMS/email + 5 demo scenarios |
| Behavioral Profiler   | User profile deviation test |
| Fraud Alerts          | Alert triage console with filters |
| Deep Analytics        | Full Plotly chart suite |
| Model Performance     | Registry table + F1/AUC bar charts |
| Risk Fusion           | Interactive multi-signal fusion builder |
| System Architecture   | ASCII diagram + engine details + API table |

---

## Tech Stack

| Layer           | Technology                          |
|-----------------|-------------------------------------|
| Backend API     | FastAPI, Pydantic v2, SQLAlchemy    |
| Database        | SQLite (default), PostgreSQL-ready  |
| ML Framework    | scikit-learn, XGBoost, SHAP         |
| NLP             | scikit-learn TF-IDF, regex          |
| Computer Vision | OpenCV                              |
| Frontend        | Streamlit, Plotly                   |
| Containerization| Docker, Docker Compose              |
| Testing         | pytest, httpx                       |

---

## Limitations

| Limitation          | Details |
|---------------------|---------|
| Synthetic Data      | Models trained on synthetic data; real-world F1 expected ~85-92% |
| QR Detection        | Requires clear, undistorted QR images; compressed screenshots may fail |
| No Auth Layer       | No JWT authentication; suitable for local/demo use only |
| Single-User SQLite  | Not suitable for concurrent production writes; use PostgreSQL |
| No Real-Time Stream | Request/response only; no Kafka/Kinesis integration |

---

## Future Roadmap

- Real dataset integration (IEEE-CIS Fraud Detection, PaySim, PhishTank)
- Graph Neural Network for money mule network detection
- JWT authentication with role-based access control
- PostgreSQL + Redis for production-grade storage
- Kafka event streaming pipeline
- Model drift monitoring (Population Stability Index)
- Champion/challenger A/B model testing framework

---

## License

MIT License -- see LICENSE file.

---

FraudShield AI is a portfolio demonstration project. Risk scores are probabilistic estimates and should not replace human judgment or official verification.
