import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from frontend.api_client import analyze_behavior
from frontend.components.kpi_card import risk_score_gauge

st.title("👤 Behavioral Anomaly Profiler")
st.caption("Analyze behavioral deviations against user baseline patterns using Isolation Forest")
st.divider()

with st.form("behavior_form"):
    col1, col2 = st.columns(2)
    with col1:
        user_id = st.text_input("User ID", value="USER_1001")
        amount = st.number_input("Transaction Amount (₹)", min_value=1.0, value=45000.0, step=500.0)
        device_id = st.text_input("Device ID", value="DEV_UNKNOWN_99")
    with col2:
        beneficiary_id = st.text_input("Beneficiary ID", value="BEN_NEW_MULE")
        location = st.text_input("Location", value="Singapore")
        hour = st.slider("Transaction Hour (24h)", 0, 23, value=3)
    
    analyze_btn = st.form_submit_button("🔍 Analyze Behavioral Pattern", type="primary", use_container_width=True)

if analyze_btn:
    from datetime import datetime
    ts = datetime.now().replace(hour=hour, minute=15)
    
    payload = {
        "user_id": user_id,
        "amount": float(amount),
        "device_id": device_id,
        "beneficiary_id": beneficiary_id if beneficiary_id else None,
        "location": location,
        "timestamp": ts.isoformat()
    }
    
    with st.spinner("Evaluating behavioral deviation against user baseline..."):
        result = analyze_behavior(payload)
    
    if "error" in result:
        st.error(f"Analysis failed: {result['error']}")
        st.stop()
    
    st.divider()
    st.subheader(f"👤 Behavioral Profile: `{result.get('user_id')}`")
    
    anom_score = result.get("behavior_anomaly_score", 0)
    is_anom = result.get("is_anomalous", False)
    profile = result.get("profile_metrics", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        risk_score_gauge(anom_score * 100, "Anomaly Score")
    with col2:
        st.metric("Anomaly Status", "⚠️ ANOMALOUS" if is_anom else "✅ NORMAL")
        st.metric("User Avg Amount", f"₹{profile.get('avg_amount', 0):,.2f}")
    with col3:
        st.metric("Active Hours Window", profile.get("normal_hours", "—"))
        st.metric("Known Devices", profile.get("known_devices_count", "—"))
    
    if is_anom:
        st.warning("⚠️ This activity deviates significantly from established user behavioral patterns.")
    else:
        st.success("✅ Activity is consistent with user's normal behavioral baseline.")
    
    st.divider()
    with st.expander("📋 Anomaly Factors Detected", expanded=True):
        reasons = result.get("anomaly_reasons", [])
        if reasons:
            for r in reasons:
                st.markdown(f"🔴 {r}")
        else:
            st.success("✅ No significant deviations from established behavioral patterns.")
