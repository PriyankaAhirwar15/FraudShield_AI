# 🛡️ FraudShield AI
### **Enterprise Multi-Signal Financial Fraud & Scam Prevention Platform**

An intelligent, full-stack AI/ML security platform engineered to detect multi-stage financial fraud, malicious phishing links, social engineering scams, and fraudulent QR payments in real time.

---

<div align="center">

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-FraudShield_App-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://fraudshield-ai-h22k.onrender.com)
[![GitHub Repo](https://img.shields.io/badge/GitHub-FraudShield_AI-181717?style=for-the-badge&logo=github)](https://github.com/PriyankaAhirwar15/FraudShield_AI)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-EB5424?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

### 🔗 **[Click Here to Launch Live Web Application (Render)](https://fraudshield-ai-h22k.onrender.com)** | **[Streamlit Mirror](https://fraudshieldai-xnvbahtway9jqzrgdx43t6.streamlit.app/)**

</div>

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

## 🚀 Quick Start (Run Locally)

### 1️⃣ Clone & Install
```bash
git clone https://github.com/PriyankaAhirwar15/FraudShield_AI.git
cd FraudShield_AI
pip install -r requirements.txt
```

### 2️⃣ Start Platform (One Command)
```bash
python run.py
```
*(Or double-click `start.bat` on Windows)*

- **Web Dashboard**: `http://localhost:8501`
- **FastAPI Swagger Docs**: `http://localhost:8000/docs`

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

---

## ☁️ Deploy to Render

You can deploy FraudShield AI directly to [Render](https://render.com) using either the **1-Service Blueprint (Free Tier)** or **Manual Web Service**:

### Option 1: Automatic Blueprint (Recommended)
1. Push your code to GitHub.
2. Log in to [Render Dashboard](https://dashboard.render.com).
3. Click **New +** → **Blueprint**.
4. Connect your `FraudShield_AI` repository.
5. Render will automatically detect `render.yaml` and configure the build & start commands!

### Option 2: Manual Web Service Setup
1. On Render Dashboard, click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Configure the following settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `chmod +x start.sh && ./start.sh`
   - **Instance Type**: `Free`
4. Add Environment Variables:
   - `PYTHON_VERSION`: `3.10.12`
   - `ENVIRONMENT`: `production`
   - `DEBUG`: `false`
   - `BACKEND_URL`: `http://127.0.0.1:8000`
5. Click **Deploy Web Service**!

---

## 🧪 Automated Tests

```bash
pytest -v
```
*(14/14 unit and integration tests passing)*

---

## 📡 API Endpoints Reference

Base URL: `http://localhost:8000/api/v1`

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health status |
| `POST` | `/fraud/predict` | Transaction fraud scoring + SHAP factor attribution |
| `POST` | `/behavior/analyze` | User behavioral anomaly evaluation |
| `POST` | `/url/scan` | Phishing URL lexical classifier |
| `POST` | `/message/analyze` | Phishing message social engineering analyzer |
| `POST` | `/qr/scan` | QR code decode and payload risk assessment |
| `POST` | `/risk/assess` | Multi-signal fusion assessment with scam chain logic |
| `GET` | `/alerts` | Paginated fraud alert triage records |
| `GET` | `/analytics/overview` | KPI overview and threat analytics |

---

## 👩‍💻 Built by Priyanka Ahirwar

**Developed by [Priyanka Ahirwar](https://github.com/PriyankaAhirwar15)**  
*AI & Machine Learning Security Engineering Project*

---

## ⚠️ Disclaimer

**FraudShield AI** is an artificial intelligence demonstration and decision-support platform designed for research, portfolio, and educational purposes. Risk scores and threat classifications represent probabilistic estimates and should not replace certified banking security protocols, AML compliance investigations, or primary human judgment.
