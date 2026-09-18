import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from frontend.api_client import scan_url
from frontend.components.kpi_card import risk_score_gauge, risk_badge

st.title("🔗 URL Phishing Scanner")
st.caption("Static lexical & ML-based malicious URL analysis — No outbound connections made to scanned URLs")
st.divider()

DEMO_URLS = [
    "http://secure-login-hdfc-kyc-update.xyz/verify",
    "http://192.168.1.105/sbi-online-portal/login.php",
    "https://bit.ly/bank-kyc-urgent-verify-now",
    "http://www.hdfc-bank-verification-update.com/login",
    "https://www.hdfcbank.com/personal/ways-to-bank/online-banking",
    "https://github.com/FraudShield-AI/docs"
]

col1, col2 = st.columns([3, 1])
with col1:
    url_input = st.text_input("🌐 Paste URL to Scan", placeholder="http://suspicious-site.xyz/banking/verify.php", label_visibility="collapsed")
with col2:
    demo_sel = st.selectbox("Try a Demo URL", ["— Select Demo —"] + DEMO_URLS, label_visibility="collapsed")

if demo_sel != "— Select Demo —":
    url_input = demo_sel

scan_btn = st.button("🔍 Scan URL", type="primary", use_container_width=True)

if scan_btn:
    if not url_input.strip():
        st.warning("Please enter or select a URL to scan.")
        st.stop()
    
    with st.spinner(f"Analyzing URL: `{url_input[:80]}...`"):
        result = scan_url(url_input.strip())
    
    if "error" in result:
        st.error(f"Scan failed: {result['error']}")
        st.stop()
    
    st.divider()
    st.subheader("🎯 URL Threat Assessment")
    
    risk_score = result.get("url_risk_score", 0)
    risk_level = result.get("risk_level", "LOW")
    domain = result.get("domain", "")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_score_gauge(risk_score, "Phishing Risk Score")
    with col2:
        st.metric("Risk Level", risk_level)
        st.markdown(risk_badge(risk_level), unsafe_allow_html=True)
    with col3:
        st.metric("Domain Analyzed", domain if domain else "—")
    
    if risk_level == "HIGH":
        st.error("🚨 **HIGH RISK URL** — Strong indicators of phishing or malicious intent detected.")
    elif risk_level == "MEDIUM":
        st.warning("⚠️ **MEDIUM RISK** — Suspicious features found. Verify before accessing.")
    else:
        st.success("✅ **LOW RISK** — No major phishing indicators detected.")
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        with st.expander("🚩 Phishing Indicators Detected", expanded=True):
            indicators = result.get("detected_indicators", [])
            if indicators:
                for ind in indicators:
                    st.markdown(f"🔴 {ind}")
            else:
                st.success("✅ No phishing indicators detected.")
    
    with col_b:
        with st.expander("🛡️ Recommended Safety Action", expanded=True):
            for i, act in enumerate(result.get("recommended_action", [])):
                st.markdown(f"**{i+1}.** {act}")
    
    with st.expander("🔬 Domain Characteristics (Feature Analysis)", expanded=False):
        import pandas as pd
        feats = result.get("domain_characteristics", {})
        if feats:
            df = pd.DataFrame([
                {"Feature": k.replace("_", " ").title(), "Value": v}
                for k, v in feats.items()
            ])
            st.dataframe(df, use_container_width=True)
    
    st.caption(f"Scanned URL: `{result.get('url', '')}` | Model: `{result.get('model_version', 'N/A')}`")
