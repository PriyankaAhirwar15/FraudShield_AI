import streamlit as st

def render_kpi_cards(kpi: dict):
    """Renders KPI summary metric cards in the dashboard header."""
    cols = st.columns(6)
    
    metrics = [
        ("Total Transactions", kpi.get("total_transactions", 0), None, "📊"),
        ("Suspicious Transactions", kpi.get("suspicious_transactions", 0), None, "⚠️"),
        ("High Risk Events", kpi.get("high_risk_events", 0), None, "🚨"),
        ("Fraud Alerts", kpi.get("fraud_alerts", 0), None, "🔔"),
        ("Avg Risk Score", f"{kpi.get('avg_risk_score', 0):.1f}", None, "📈"),
        ("Prevented Loss (₹)", f"₹{kpi.get('estimated_prevented_loss', 0):,.0f}", None, "💰"),
    ]
    
    for col, (label, value, delta, icon) in zip(cols, metrics):
        with col:
            st.metric(label=f"{icon} {label}", value=value, delta=delta)

def risk_badge(risk_level: str) -> str:
    """Returns HTML badge string for a given risk level."""
    colors = {"HIGH": "#e74c3c", "MEDIUM": "#f39c12", "LOW": "#27ae60"}
    color = colors.get(risk_level.upper(), "#95a5a6")
    return f'<span style="background-color:{color};color:white;padding:3px 10px;border-radius:12px;font-weight:bold;font-size:13px">{risk_level}</span>'

def risk_score_gauge(score: float, label: str = "Risk Score"):
    """Renders a color-coded risk score using native Streamlit metrics + progress."""
    if score >= 70:
        color = "inverse"
        level = "HIGH"
    elif score >= 40:
        color = "off"
        level = "MEDIUM"
    else:
        color = "normal"
        level = "LOW"
    
    st.metric(label=label, value=f"{score:.1f} / 100", delta=level, delta_color=color)
    st.progress(score / 100.0)
