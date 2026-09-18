import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from frontend.api_client import get_model_registry

st.title('🔬 Model Performance Registry')
st.caption('Trained ML model benchmarks, hyperparameters, and training metadata')
st.divider()

with st.spinner('Loading model registry...'):
    data = get_model_registry()

if 'error' in data:
    st.error(f"Backend unreachable: {data['error']}")
    st.stop()

benchmarks = data.get('benchmarks', [])
active_models = data.get('active_models', {})

if not benchmarks:
    st.warning('No model benchmarks found in registry. Run: python scripts/train_models.py')
    st.stop()

rows = []
for b in benchmarks:
    rows.append({
        'Model Name': b.get('model_name', ''),
        'Model Type': b.get('model_type', ''),
        'Version': b.get('model_version', '1.0.0'),
        'Precision': f"{b.get('precision', 0):.4f}",
        'Recall': f"{b.get('recall', 0):.4f}",
        'F1 Score': f"{b.get('f1_score', 0):.4f}",
        'ROC-AUC': f"{b.get('roc_auc', 0):.4f}",
        'Training Date': str(b.get('training_date', ''))[:19]
    })

df = pd.DataFrame(rows)
st.subheader('📋 Model Benchmark Comparison')
st.dataframe(df, use_container_width=True, height=340)

st.divider()

st.subheader('📊 Model Metric Comparison (F1 Score and ROC-AUC)')
names = [b.get('model_name', '') for b in benchmarks]
f1s   = [b.get('f1_score', 0) for b in benchmarks]
aucs  = [b.get('roc_auc', 0) for b in benchmarks]

fig = go.Figure()
fig.add_trace(go.Bar(name='F1 Score', x=names, y=f1s, marker_color='#3498db', text=[f'{v:.4f}' for v in f1s], textposition='outside'))
fig.add_trace(go.Bar(name='ROC-AUC', x=names, y=aucs, marker_color='#2ecc71', text=[f'{v:.4f}' for v in aucs], textposition='outside'))
fig.update_layout(
    barmode='group',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    height=400,
    yaxis=dict(range=[0, 1.15]),
    margin=dict(l=20, r=20, t=20, b=100),
    legend=dict(orientation='h', y=-0.35)
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader('⚡ Active Deployed Models')
for k, v in active_models.items():
    st.info(f"**{k.replace('_', ' ').title()}**: Version `{v}` (Active in Production Pipeline)")

st.caption('⚠️ Note: Benchmark metrics were evaluated on synthetic test partitions. In real-world noisy production environments, scores will be lower and subject to data drift.')
