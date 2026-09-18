import streamlit as st

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
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a0e1a 0%, #0d1527 50%, #0a1020 100%);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1527 0%, #0a0e1a 100%);
        border-right: 1px solid rgba(52, 152, 219, 0.2);
    }
    
    [data-testid="stSidebar"] * {
        color: #cdd6f4 !important;
    }
    
    /* Metric Cards */
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
    
    /* Headers */
    h1 { color: #89b4fa !important; font-weight: 700 !important; }
    h2 { color: #cdd6f4 !important; font-weight: 600 !important; }
    h3 { color: #a6e3a1 !important; font-weight: 600 !important; }
    
    /* Buttons */
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
    
    /* Expander */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(52, 152, 219, 0.3) !important;
        border-radius: 8px !important;
        color: #cdd6f4 !important;
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(52, 152, 219, 0.3) !important;
        color: #cdd6f4 !important;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(52, 152, 219, 0.3) !important;
        color: #cdd6f4 !important;
        border-radius: 8px !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #27ae60, #f39c12, #e74c3c) !important;
        border-radius: 999px;
    }
    
    /* Divider */
    hr { border-color: rgba(255, 255, 255, 0.1) !important; }
    
    /* Alert boxes */
    .stAlert { border-radius: 10px !important; }
    
    /* DataFrame */
    [data-testid="stDataFrame"] { border-radius: 10px; }
    
    /* Main container padding */
    .main .block-container { padding-top: 1.5rem; }
    
    /* Plotly charts background transparency */
    .js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🛡️ FraudShield AI")
    st.markdown("*Enterprise Fraud & Scam Prevention*")
    st.divider()
    
    from frontend.api_client import health_check
    health = health_check()
    if "error" in health:
        st.error(f"⚠️ Backend Offline")
        st.caption("Start with: `uvicorn app.main:app --reload`")
    else:
        st.success(f"✅ Backend Online")
        st.caption(f"v{health.get('version', '1.0.0')} — {health.get('environment', 'dev').title()}")
    
    st.divider()
    st.caption("**Navigation**")
    st.markdown("""
    - 📊 Dashboard
    - 💳 Transaction Scanner
    - 🔗 URL Scanner
    - 📷 QR / Image Scanner
    - ✉️ Message Analyzer
    - 👤 Behavioral Profiler
    - 🚨 Fraud Alerts
    - 📈 Deep Analytics
    - 🔬 Model Performance
    - ℹ️ System Architecture
    """)
    
    st.divider()
    st.caption("⚠️ **Disclaimer**: FraudShield AI is a decision-support platform. Risk scores indicate *potential* threats. Always verify through official channels before taking action.")

# Default landing
st.title("🛡️ FraudShield AI")
st.subheader("Enterprise Multi-Signal Financial Fraud & Scam Prevention Platform")
st.markdown("""
Welcome to **FraudShield AI** — select a module from the sidebar pages to begin.

| Module | Purpose |
|--------|---------|
| 📊 Dashboard | Real-time KPIs, fraud trends, and recent alerts |
| 💳 Transaction Scanner | ML-powered transaction fraud scoring & SHAP explanation |
| 🔗 URL Scanner | Phishing URL lexical & ML classifier |
| 📷 QR / Image Scanner | QR decode, UPI analysis, crypto address detection |
| ✉️ Message Analyzer | SMS/Email/WhatsApp phishing detection |
| 🚨 Fraud Alerts | Alert triage and investigation console |
| 📈 Deep Analytics | Advanced fraud analytics and pattern visualizations |
| 🔬 Model Performance | ML model benchmark comparison and registry |
""")
