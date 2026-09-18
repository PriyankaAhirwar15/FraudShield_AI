import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List

COLORS = {
    "HIGH": "#e74c3c",
    "MEDIUM": "#f39c12",
    "LOW": "#27ae60",
    "primary": "#3498db",
    "dark": "#1a1f36"
}

def fraud_trend_chart(trends: List[Dict]) -> go.Figure:
    df = pd.DataFrame(trends)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["total_events"],
        name="All Events", fill="tonexty",
        line=dict(color=COLORS["primary"], width=2),
        fillcolor="rgba(52, 152, 219, 0.15)"
    ))
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["flagged_threats"],
        name="Flagged Threats", fill="tozeroy",
        line=dict(color=COLORS["HIGH"], width=2.5),
        fillcolor="rgba(231, 76, 60, 0.2)"
    ))
    fig.update_layout(
        title="Threat Detection Trend (Last 8 Days)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        legend=dict(orientation="h", y=-0.15),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def risk_distribution_donut(risk_dist: Dict) -> go.Figure:
    labels = list(risk_dist.keys())
    values = list(risk_dist.values())
    colors = [COLORS.get(k, "#95a5a6") for k in labels]
    
    fig = go.Figure(go.Pie(
        labels=labels, values=values,
        hole=0.55, marker=dict(colors=colors),
        textinfo="percent+label",
        hovertemplate="%{label}: %{value:,} events<br>%{percent}<extra></extra>"
    ))
    fig.update_layout(
        title="Risk Level Distribution",
        paper_bgcolor="rgba(0,0,0,0)",
        height=300,
        showlegend=True,
        legend=dict(orientation="h", y=-0.1),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def fraud_by_type_bar(type_dict: Dict) -> go.Figure:
    df = pd.DataFrame(list(type_dict.items()), columns=["Type", "Count"])
    df = df.sort_values("Count", ascending=False)
    
    fig = px.bar(
        df, x="Type", y="Count",
        color="Type",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Suspicious Events by Transaction Type",
        text="Count"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title="", yaxis_title="Count"
    )
    fig.update_traces(textposition="outside")
    return fig

def fraud_by_hour_heatmap(hour_data: Dict) -> go.Figure:
    hours = sorted(hour_data.keys())
    values = [hour_data[h] for h in hours]
    
    fig = go.Figure(go.Bar(
        x=[f"{h:02d}:00" for h in hours],
        y=values,
        marker=dict(
            color=values,
            colorscale=[[0, "#27ae60"], [0.5, "#f39c12"], [1.0, "#e74c3c"]],
            showscale=True,
            colorbar=dict(title="Events")
        )
    ))
    fig.update_layout(
        title="Fraud Events by Hour of Day",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=280,
        xaxis_title="Hour",
        yaxis_title="Suspicious Events",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def location_bar(location_data: Dict) -> go.Figure:
    df = pd.DataFrame(list(location_data.items()), columns=["Location", "Events"])
    df = df.sort_values("Events", ascending=True)
    
    fig = px.bar(
        df, x="Events", y="Location", orientation="h",
        title="Geographic Activity Distribution",
        color="Events",
        color_continuous_scale=["#27ae60", "#f39c12", "#e74c3c"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False
    )
    return fig

def scam_channel_pie(channel_data: Dict) -> go.Figure:
    fig = go.Figure(go.Pie(
        labels=list(channel_data.keys()),
        values=list(channel_data.values()),
        hole=0.4,
        textinfo="percent+label",
        marker=dict(colors=["#e74c3c", "#f39c12", "#9b59b6", "#3498db"])
    ))
    fig.update_layout(
        title="Scam Attack Channel Breakdown",
        paper_bgcolor="rgba(0,0,0,0)",
        height=280,
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=10, r=10, t=40, b=10)
    )
    return fig

def shap_waterfall_chart(factors: List[Dict]) -> go.Figure:
    top = factors[:8]
    names = [f["display_name"] for f in top]
    values = [f["shap_impact"] for f in top]
    colors = [COLORS["HIGH"] if v > 0 else COLORS["LOW"] for v in values]
    
    fig = go.Figure(go.Bar(
        x=values,
        y=names,
        orientation="h",
        marker=dict(color=colors),
        text=[f"+{v:.3f}" if v > 0 else f"{v:.3f}" for v in values],
        textposition="outside"
    ))
    fig.update_layout(
        title="SHAP Feature Impact (Top Factors Driving Risk Score)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        xaxis_title="SHAP Impact (→ increases risk)",
        margin=dict(l=20, r=80, t=40, b=20)
    )
    return fig
