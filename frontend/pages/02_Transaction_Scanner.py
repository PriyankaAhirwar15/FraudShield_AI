import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
from datetime import datetime
from frontend.api_client import predict_transaction
from frontend.components.kpi_card import risk_score_gauge, risk_badge
from frontend.components.charts import shap_waterfall_chart

st.title("💳 Transaction Fraud Scanner")
st.caption("ML-powered transaction risk analysis with SHAP explainability")
st.divider()

with st.form("transaction_form", clear_on_submit=False):
    st.subheader("📋 Transaction Details")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        user_id = st.text_input("User ID", value="USER_1042", help="Customer identifier")
        amount = st.number_input("Amount (₹)", min_value=1.0, max_value=10000000.0, value=75000.0, step=100.0)
    with col2:
        txn_type = st.selectbox("Transaction Type", ["TRANSFER", "PAYMENT", "CASH_OUT", "DEBIT"])
        device_id = st.text_input("Device ID", value="DEV_NEW_88912")
    with col3:
        location = st.text_input("Location", value="Lagos, NG")
        beneficiary_id = st.text_input("Beneficiary ID", value="BEN_UNKNOWN_997")
    
    st.subheader("📊 User Historical Baseline")
    col4, col5, col6 = st.columns(3)
    with col4:
        historical_avg = st.number_input("Historical Avg Amount (₹)", value=1500.0, min_value=50.0)
    with col5:
        account_age = st.number_input("Account Age (Days)", value=180, min_value=1)
    with col6:
        txn_hour = st.slider("Transaction Hour (24h)", 0, 23, value=2)

    st.divider()
    submit = st.form_submit_button("🔍 Scan Transaction", type="primary", use_container_width=True)

if submit:
    ts = datetime.now().replace(hour=txn_hour, minute=30)
    payload = {
        "user_id": user_id,
        "amount": float(amount),
        "transaction_type": txn_type,
        "device_id": device_id,
        "beneficiary_id": beneficiary_id,
        "location": location,
        "account_age_days": int(account_age),
        "historical_avg_amount": float(historical_avg),
        "timestamp": ts.isoformat()
    }
    
    with st.spinner("🔄 Analyzing transaction through fraud models..."):
        result = predict_transaction(payload)
    
    if "error" in result:
        st.error(f"Scan failed: {result['error']}")
        st.stop()
    
    # ── Results ─────────────────────────────────────────────────────
    st.divider()
    st.subheader("🎯 Fraud Assessment Results")
    
    risk_score = result.get("risk_score", 0)
    risk_level = result.get("risk_level", "LOW")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        risk_score_gauge(risk_score, "Final Risk Score")
    with col2:
        st.metric("Risk Level", risk_level)
        st.markdown(risk_badge(risk_level), unsafe_allow_html=True)
    with col3:
        st.metric("Fraud Probability", f"{result.get('fraud_probability', 0):.1%}")
    with col4:
        st.metric("Behavior Anomaly", f"{result.get('behavior_anomaly_score', 0):.1%}")
    
    if risk_level == "HIGH":
        st.error("🚨 **HIGH RISK DETECTED** — Potential fraud activity identified. Review recommended actions immediately.")
    elif risk_level == "MEDIUM":
        st.warning("⚠️ **MEDIUM RISK** — Suspicious indicators present. Proceed with caution and verify transaction details.")
    else:
        st.success("✅ **LOW RISK** — Transaction appears consistent with normal user patterns.")
    
    st.divider()
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        with st.expander("🔍 Why was this flagged? (Risk Reasons)", expanded=True):
            reasons = result.get("reasons", [])
            for i, r in enumerate(reasons):
                icon = "🔴" if risk_level == "HIGH" else "🟡"
                st.markdown(f"{icon} {r}")
    
    with col_b:
        with st.expander("🛡️ Recommended Safety Actions", expanded=True):
            actions = result.get("recommended_action", [])
            for i, a in enumerate(actions):
                st.markdown(f"**{i+1}.** {a}")
    
    # SHAP factors
    factors = result.get("contributing_factors", [])
    if factors and len(factors) > 0:
        st.subheader("📊 SHAP Feature Impact (Explainability)")
        st.caption("Factors that contributed most to the risk score (SHAP attribution values)")
        fig = shap_waterfall_chart(factors)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 Full Feature Attribution Table"):
            import pandas as pd
            df = pd.DataFrame(factors)
            df["Risk Impact"] = df["increases_risk"].apply(lambda x: "⬆️ Increases Risk" if x else "⬇️ Reduces Risk")
            st.dataframe(
                df[["display_name", "actual_value", "shap_impact", "Risk Impact"]].rename(columns={
                    "display_name": "Feature",
                    "actual_value": "Value",
                    "shap_impact": "SHAP Impact",
                }),
                use_container_width=True
            )
    
    st.caption(f"Model: `{result.get('model_version', 'N/A')}` | Transaction: `{result.get('transaction_id', 'N/A')}`")
