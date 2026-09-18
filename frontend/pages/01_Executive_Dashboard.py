import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import pandas as pd
from frontend.api_client import get_analytics, get_alerts
from frontend.components.kpi_card import render_kpi_cards, risk_badge
from frontend.components.charts import (
    fraud_trend_chart, risk_distribution_donut, fraud_by_type_bar,
    fraud_by_hour_heatmap, location_bar, scam_channel_pie
)

st.title("📊 Executive Security Dashboard")
st.caption("Real-time threat intelligence summary across all detection engines")
st.divider()

# ── Load Analytics Data ──────────────────────────────────────────────
with st.spinner("Loading threat intelligence data..."):
    data = get_analytics()

if "error" in data:
    st.error(f"⚠️ Backend unreachable: {data['error']}")
    st.info("Start the FastAPI backend: `uvicorn app.main:app --reload`")
    st.stop()

kpi = data.get("kpi", {})
trends = data.get("fraud_trends_timeline", [])
type_dist = data.get("fraud_by_transaction_type", {})
hour_dist = data.get("fraud_by_hour", {})
location_dist = data.get("fraud_by_location", {})
risk_dist = data.get("risk_distribution", {})
channel_dist = data.get("scam_channel_breakdown", {})

# ── KPI Cards ────────────────────────────────────────────────────────
render_kpi_cards(kpi)

st.divider()

# ── Charts Row 1 ─────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
with col1:
    if trends:
        st.plotly_chart(fraud_trend_chart(trends), use_container_width=True)
with col2:
    if risk_dist:
        st.plotly_chart(risk_distribution_donut(risk_dist), use_container_width=True)

# ── Charts Row 2 ─────────────────────────────────────────────────────
col3, col4 = st.columns(2)
with col3:
    if type_dist:
        st.plotly_chart(fraud_by_type_bar(type_dist), use_container_width=True)
with col4:
    if hour_dist:
        st.plotly_chart(fraud_by_hour_heatmap(hour_dist), use_container_width=True)

# ── Charts Row 3 ─────────────────────────────────────────────────────
col5, col6 = st.columns(2)
with col5:
    if location_dist:
        st.plotly_chart(location_bar(location_dist), use_container_width=True)
with col6:
    if channel_dist:
        st.plotly_chart(scam_channel_pie(channel_dist), use_container_width=True)

st.divider()

# ── Recent Alerts Table ───────────────────────────────────────────────
st.subheader("🔔 Recent Fraud Alerts")

alerts_data = get_alerts(limit=10)
if isinstance(alerts_data, list) and alerts_data:
    rows = []
    for a in alerts_data:
        rows.append({
            "Alert ID": a.get("alert_id", ""),
            "Event Type": a.get("event_type", ""),
            "Risk Score": f"{a.get('risk_score', 0):.1f}",
            "Risk Level": a.get("risk_level", ""),
            "Status": a.get("status", ""),
            "Created At": str(a.get("created_at", ""))[:19]
        })
    df = pd.DataFrame(rows)
    
    def style_risk(val):
        colors = {"HIGH": "color: #e74c3c; font-weight: bold",
                  "MEDIUM": "color: #f39c12; font-weight: bold",
                  "LOW": "color: #27ae60"}
        return colors.get(val, "")
    
    styled = df.style.applymap(style_risk, subset=["Risk Level"])
    st.dataframe(styled, use_container_width=True, height=320)
else:
    st.info("No alerts found. Run some scans to generate fraud alert records.")
