import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if FRONTEND_DIR not in sys.path:
    sys.path.insert(0, FRONTEND_DIR)

import streamlit as st
from frontend.api_client import get_analytics
from frontend.components.charts import (
    fraud_trend_chart, risk_distribution_donut,
    fraud_by_type_bar, fraud_by_hour_heatmap,
    location_bar, scam_channel_pie
)

st.title("📈 Deep Analytics")
st.caption("Comprehensive fraud pattern visualizations and statistical breakdowns")
st.divider()

with st.spinner("Loading analytics data..."):
    data = get_analytics()

if "error" in data:
    st.error(f"Backend unreachable: {data['error']}")
    st.stop()

kpi       = data.get("kpi", {})
trends    = data.get("fraud_trends_timeline", [])
type_dist = data.get("fraud_by_transaction_type", {})
hour_dist = data.get("fraud_by_hour", {})
loc_dist  = data.get("fraud_by_location", {})
risk_dist = data.get("risk_distribution", {})
ch_dist   = data.get("scam_channel_breakdown", {})

# KPI summary
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Transactions", kpi.get("total_transactions",0))
c2.metric("Suspicious", kpi.get("suspicious_transactions",0))
c3.metric("High Risk", kpi.get("high_risk_events",0))
c4.metric("Avg Risk Score", f"{kpi.get('avg_risk_score',0):.1f}")
c5.metric("Detection Rate", f"{kpi.get('fraud_detection_rate',0):.1%}" if kpi.get('fraud_detection_rate') else "—")

st.divider()

st.subheader("🗓️ Threat Timeline")
if trends:
    st.plotly_chart(fraud_trend_chart(trends), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Risk Distribution")
    if risk_dist:
        st.plotly_chart(risk_distribution_donut(risk_dist), use_container_width=True)

with col2:
    st.subheader("🎭 Scam Attack Channels")
    if ch_dist:
        st.plotly_chart(scam_channel_pie(ch_dist), use_container_width=True)

col3, col4 = st.columns(2)
with col3:
    st.subheader("💳 Fraud by Transaction Type")
    if type_dist:
        st.plotly_chart(fraud_by_type_bar(type_dist), use_container_width=True)

with col4:
    st.subheader("🕐 Fraud Events by Hour")
    if hour_dist:
        st.plotly_chart(fraud_by_hour_heatmap(hour_dist), use_container_width=True)

st.subheader("🌍 Geographic Distribution")
if loc_dist:
    st.plotly_chart(location_bar(loc_dist), use_container_width=True)

# Insight callouts
st.divider()
st.subheader("💡 AI-Detected Fraud Insights")
insights = data.get("insights", [])
if insights:
    for insight in insights:
        severity = insight.get("severity","LOW")
        icon = "🔴" if severity=="HIGH" else ("🟡" if severity=="MEDIUM" else "🟢")
        st.info(f"{icon} **{insight.get('insight_type','').replace('_',' ').title()}** — {insight.get('description','')}")
else:
    st.info("ℹ️ Insights will appear as more transactions are scanned.")