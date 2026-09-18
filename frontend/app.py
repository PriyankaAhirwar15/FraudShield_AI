import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
FRONTEND_DIR = os.path.abspath(os.path.dirname(__file__))
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

import streamlit as st

try:
    from frontend.api_client import health_check
except ImportError:
    from api_client import health_check

st.set_page_config(
    page_title="FraudShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "**FraudShield AI** — Enterprise Multi-Signal Financial Fraud & Scam Prevention Platform"
    }
)

# Global Dark Theme Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1527 50%, #0a1020 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1527 0%, #0a0e1a 100%);
        border-right: 1px solid rgba(52, 152, 219, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #cdd6f4 !important;
    }
    
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(52, 152, 219, 0.2);
        border-radius: 12px;
        padding: 12px 16px;
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 500;
        color: #89b4fa !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 22px !important;
        font-weight: 700;
        color: #cdd6f4 !important;
    }
    
    h1 { color: #89b4fa !important; font-weight: 700 !important; }
    h2 { color: #cdd6f4 !important; font-weight: 600 !important; }
    h3 { color: #a6e3a1 !important; font-weight: 600 !important; }
    
    .stButton > button {
        background: linear-gradient(135deg, #3498db, #1a6fa8) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2980b9, #1a5a8a) !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4) !important;
        transform: translateY(-1px);
    }
    
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(52, 152, 219, 0.3) !important;
        border-radius: 8px !important;
        color: #cdd6f4 !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(52, 152, 219, 0.3) !important;
        color: #cdd6f4 !important;
        border-radius: 8px !important;
    }
    
    .stProgress > div > div {
        background: linear-gradient(90deg, #27ae60, #f39c12, #e74c3c) !important;
        border-radius: 999px;
    }
    
    hr { border-color: rgba(255, 255, 255, 0.1) !important; }
    .stAlert { border-radius: 10px !important; }
    [data-testid="stDataFrame"] { border-radius: 10px; }
    .main .block-container { padding-top: 1.5rem; }
    .js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🛡️ FraudShield AI")
    st.markdown("*Enterprise Fraud & Scam Prevention*")
    st.divider()
    
    health = health_check()
    if "error" in health:
        st.error("⚠️ Backend Offline")
        st.caption("Start with: `uvicorn app.main:app --reload`")
    else:
        st.success("✅ Backend Online")
        st.caption(f"v{health.get('version', '1.0.0')} — {health.get('environment', 'dev').title()}")
    
    st.divider()
    st.caption("**Navigation Modules**")
    st.markdown("""
    - 📊 **01** Executive Dashboard
    - 💳 **02** Transaction Scanner
    - 🔗 **03** URL Phishing Scanner
    - 📷 **04** QR Image Scanner
    - ✉️ **05** Message Analyzer
    - 👤 **06** Behavioral Profiler
    - 🚨 **07** Fraud Alerts Console
    - 📈 **08** Deep Analytics
    - 🔬 **09** Model Performance
    - ℹ️ **10** System Architecture
    - 🔀 **11** Risk Fusion
    """)
    
    st.divider()
    st.caption("⚠️ **Disclaimer**: FraudShield AI is a decision-support platform. Always verify through official banking channels.")

# Default landing page
st.title("🛡️ FraudShield AI")
st.subheader("Enterprise Multi-Signal Financial Fraud & Scam Prevention Platform")
st.markdown("""
Welcome to **FraudShield AI** — an end-to-end intelligent security platform that detects financial fraud and scam patterns across multiple attack surfaces.

### 🧭 Select a Module from the Left Sidebar:

| Module | Purpose |
| :--- | :--- |
| 📊 **01 Executive Dashboard** | Real-time threat intelligence, KPIs, 8-day velocity timeline & geographic alerts |
| 💳 **02 Transaction Scanner** | Supervised XGBoost fraud risk inference with interactive **SHAP explainability** |
| 🔗 **03 URL Phishing Scanner** | Safe static lexical analysis across 17 URL & domain threat features |
| 📷 **04 QR / Image Scanner** | Computer Vision QR decode, UPI analysis, crypto detection & link scanner chaining |
| ✉️ **05 Message Analyzer** | NLP social engineering classifier detecting urgency, threats & impersonation |
| 👤 **06 Behavioral Profiler** | Unsupervised Isolation Forest detecting anomalies against 30-day user baselines |
| 🚨 **07 Fraud Alerts** | Investigation console for alert triage and lifecycle management |
| 📈 **08 Deep Analytics** | Comprehensive Plotly breakdowns across transaction types, hours & channels |
| 🔬 **09 Model Performance** | Benchmark comparison matrix and model registry |
| ℹ️ **10 System Architecture** | Interactive architecture diagrams and REST API documentation |
| 🔀 **11 Risk Fusion** | Multi-signal weighted fusion engine simulating **multi-stage scam chains** |
""")
