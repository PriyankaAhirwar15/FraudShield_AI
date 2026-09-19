import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

import streamlit as st
from frontend.api_client import analyze_message
from frontend.components.kpi_card import risk_score_gauge, risk_badge

st.title("✉️ Phishing Message Analyzer")
st.caption("SMS / Email / WhatsApp social engineering scam detection powered by NLP classifier")
st.divider()

DEMO_MESSAGES = {
    "High Risk — Bank KYC Scam": "Dear Customer, your HDFC Bank account is suspended today due to pending KYC. Click http://bit.ly/bank-kyc-verify to update PAN immediately or your account will be permanently blocked.",
    "High Risk — Income Tax Refund Fraud": "Income Tax Refund of Rs 18,450 approved. Update your bank account details now at http://192.168.1.10/refund/login to receive funds within 24 hours.",
    "High Risk — Reverse UPI Scam": "Congratulations! Your refund of Rs 5,000 has been processed. Please scan the attached QR code to receive your money directly in your bank account.",
    "Medium Risk — Suspicious Lottery": "You have been selected for KBC Season 17 lucky draw! Your prize of Rs 25,00,000 is waiting for collection. Call 9876543210 to claim.",
    "Low Risk — Legitimate Bank SMS": "Dear customer, Rs 2,450 credited to your account XX4821 via NEFT from Employer Pvt Ltd. Txn Ref: HDFC12345. Balance: Rs 48,210.",
}

channel = st.selectbox("Message Channel", ["SMS", "EMAIL", "WHATSAPP"])

tab1, tab2 = st.tabs(["✏️ Enter Message", "📋 Demo Messages"])

with tab1:
    message_input = st.text_area(
        "Paste suspicious message here",
        placeholder="Paste SMS / Email / WhatsApp message text for analysis...",
        height=180,
        label_visibility="collapsed"
    )
    analyze_btn = st.button("🔍 Analyze Message", type="primary", use_container_width=True)

with tab2:
    selected_demo = st.selectbox("Select Demo Scenario", list(DEMO_MESSAGES.keys()))
    st.info(f"**Preview:** {DEMO_MESSAGES[selected_demo][:200]}...")
    demo_btn = st.button("Analyze Demo Message", type="secondary", use_container_width=True)
    if demo_btn:
        message_input = DEMO_MESSAGES[selected_demo]
        analyze_btn = True

if (analyze_btn or demo_btn) and message_input:
    with st.spinner("🔄 Analyzing message with NLP classifier..."):
        result = analyze_message(message_input.strip(), channel)
    
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
        st.stop()
    
    st.divider()
    st.subheader("🎯 Phishing Risk Assessment")
    
    risk_score = result.get("phishing_risk_score", 0)
    risk_level = result.get("risk_level", "LOW")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        risk_score_gauge(risk_score, "Phishing Risk Score")
    with col2:
        st.metric("Risk Level", risk_level)
        st.markdown(risk_badge(risk_level), unsafe_allow_html=True)
    with col3:
        indicators = []
        if result.get("urgency_detected"): indicators.append("⚠️ Urgency")
        if result.get("impersonation_detected"): indicators.append("🎭 Impersonation")
        if result.get("threat_detected"): indicators.append("💀 Threat")
        st.metric("Patterns Detected", len(indicators))
        for ind in indicators: st.caption(ind)
    with col4:
        urls = result.get("extracted_urls", [])
        st.metric("Embedded Links Found", len(urls))
        for u in urls[:2]: st.caption(f"🔗 `{u[:45]}...`" if len(u) > 45 else f"🔗 `{u}`")
    
    if risk_level == "HIGH":
        st.error("🚨 **HIGH RISK MESSAGE** — This message contains multiple phishing/scam indicators.")
    elif risk_level == "MEDIUM":
        st.warning("⚠️ **MEDIUM RISK** — This message has some suspicious patterns. Verify sender.")
    else:
        st.success("✅ **LOW RISK** — No strong phishing indicators detected.")
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    with col_a:
        with st.expander("🚩 Social Engineering Indicators", expanded=True):
            dets = result.get("detected_indicators", [])
            if dets:
                for d in dets: st.markdown(f"🔴 {d}")
            else:
                st.success("✅ No phishing patterns detected.")
    
    with col_b:
        with st.expander("🛡️ Recommended Action", expanded=True):
            for i, act in enumerate(result.get("recommended_action", [])):
                st.markdown(f"**{i+1}.** {act}")
    
    st.caption(f"Message ID: `{result.get('message_id', 'N/A')}` | Model: `{result.get('model_version', 'N/A')}`")

elif (analyze_btn or demo_btn) and not message_input:
    st.warning("Please enter a message to analyze.")