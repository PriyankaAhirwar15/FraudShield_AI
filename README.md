# 🛡️ FraudShield AI
### **Enterprise Multi-Signal Financial Fraud & Scam Prevention Platform**

An intelligent, full-stack AI/ML security platform engineered to detect multi-stage financial fraud, malicious phishing links, social engineering scams, and fraudulent QR payments in real time.

---

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.60+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB5424?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 🌟 Overview

Modern cyber fraud operates in coordinated stages:
$$\text{Phishing Message} \longrightarrow \text{Malicious URL} \longrightarrow \text{Fake Payment QR} \longrightarrow \text{Fraudulent Transaction}$$

**FraudShield AI** combines 5 specialized detection engines through an adaptive **Multi-Signal Fusion Engine** with **SHAP explainability** and prescriptive safety actions.

---

## ⚡ Core Detection Engines

| Engine | Technology | Capabilities |
| :--- | :--- | :--- |
| 💳 **Transaction Fraud** | `XGBoost` + `SHAP TreeExplainer` | Real-time financial scoring with per-factor SHAP explainability waterfall |
| 👤 **Behavioral Anomaly** | `Isolation Forest` (Unsupervised) | Flags deviations from 30-day user baselines (nocturnal activity, novel devices/beneficiaries) |
| 🔗 **Phishing URL Scanner** | `Random Forest` Lexical NLP | Static analysis across 17 lexical & entropy domain threat indicators |
| ✉️ **Message Analyzer** | `TF-IDF` + `Logistic Regression` | Detects social engineering urgency, authority impersonation & OTP harvesting |
| 📷 **QR / Image Scanner** | `OpenCV QRCodeDetector` | Decodes QR payloads, detects fraudulent UPI IDs, crypto traps & chains to URL scanner |
| 🔀 **Risk Fusion** | Weighted Adaptive Ensemble | Cross-vector score fusion with **Scam Chain Escalation** ($\ge 85$ Critical Policy) |

---

## 🏗️ Architecture

```
STREAMLIT DASHBOARD (Port 8501)
 ├── 📊 Executive Dashboard    ├── 👤 Behavioral Profiler    ├── 🔀 Risk Fusion
 ├── 💳 Transaction Scanner    ├── 🚨 Fraud Alerts Console   ├── 🔬 Model Performance
 ├── 🔗 URL Phishing Scanner   ├── 📈 Deep Analytics         └── ℹ️ System Architecture
 └── 📷 QR Image Scanner       └── ✉️ Message Analyzer
               │
               ▼  HTTP REST API
FASTAPI BACKEND ENGINE (Port 8000)
 ├── /fraud/predict            ├── /url/scan                 ├── /risk/assess
 ├── /behavior/analyze         ├── /message/analyze          └── /analytics/overview
               │
               ▼
ML SERVICES & STORAGE
 ├── XGBoost + SHAP TreeExplainer    ├── Random Forest & Isolation Forest
 └── SQLite / PostgreSQL DB          └── Scikit-Learn TF-IDF NLP Pipeline
```

---

## 🚀 Quick Start

### 1️⃣ Clone & Install
```bash
git clone https://github.com/PriyankaAhirwar15/FraudShield_AI.git
cd FraudShield_AI
pip install -r requirements.txt
```

### 2️⃣ Start the Entire Platform (One Command)
```bash
python run.py
```
*(Or double-click `start.bat` on Windows)*

- 🌐 **Streamlit UI Dashboard**: `http://localhost:8501`
- 📖 **FastAPI Swagger Docs**: `http://localhost:8000/docs`

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## 🧪 Automated Tests

```bash
pytest -v
```
*(14/14 unit and integration tests passing)*

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/v1/health` | Service health status |
| `POST` | `/api/v1/fraud/predict` | Transaction fraud scoring + SHAP factor attribution |
| `POST` | `/api/v1/behavior/analyze` | User behavioral anomaly evaluation |
| `POST` | `/api/v1/url/scan` | Phishing URL lexical classifier |
| `POST` | `/api/v1/message/analyze` | Phishing message social engineering analyzer |
| `POST` | `/api/v1/qr/scan` | QR code decode and payload risk assessment |
| `POST` | `/api/v1/risk/assess` | Multi-signal fusion assessment with scam chain logic |
| `GET` | `/api/v1/alerts` | Paginated fraud alert triage records |
| `GET` | `/api/v1/analytics/overview` | KPI overview and threat analytics |

---

## 👩‍💻 Built by Priyanka Ahirwar

**Developed by [Priyanka Ahirwar](https://github.com/PriyankaAhirwar15)**  
*AI & Machine Learning Security Engineering Project*

---

## ⚠️ Disclaimer

**FraudShield AI** is an artificial intelligence demonstration and decision-support platform designed for research, portfolio, and educational purposes. Risk scores and threat classifications represent probabilistic estimates and should not replace certified banking security protocols, AML compliance investigations, or primary human judgment.
