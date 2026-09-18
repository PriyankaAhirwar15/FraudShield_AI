import os

p9 = """import sys, os
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
"""

p11 = """import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import streamlit as st
from datetime import datetime
from frontend.api_client import assess_risk_fusion
from frontend.components.kpi_card import risk_score_gauge, risk_badge

st.title('🔀 Multi-Signal Risk Fusion Engine')
st.caption('Evaluate coordinated multi-vector fraud & scam threats across transactions, URLs, messages, and QR codes')
st.divider()

st.info('💡 Multi-stage scams combine social engineering (phishing SMS/Email), malicious links/QRs, and abnormal transactions. This engine fuses all signals with dynamic weighting and escalation rules.')

with st.form('fusion_form'):
    st.subheader('1. Phishing & Social Engineering Signals')
    c1, c2 = st.columns(2)
    with c1:
        include_msg = st.checkbox('Include Phishing Message / SMS', value=True)
        msg_text = st.text_area(
            'Message Content',
            value='Dear customer, your bank account is blocked due to KYC. Update immediately at http://secure-login-hdfc-kyc-update.xyz/verify or funds frozen.',
            height=100
        )
    with c2:
        include_url = st.checkbox('Include Malicious / Phishing URL', value=True)
        url_text = st.text_input('Scanned URL', value='http://secure-login-hdfc-kyc-update.xyz/verify')
        include_qr = st.checkbox('Include QR Code Payload', value=False)
        qr_text = st.text_input('QR Decoded Payload', value='upi://pay?pa=refund_support_kyc@upi&pn=Tax+Refund+Desk&am=25000')

    st.subheader('2. Financial Transaction & Behavioral Signal')
    include_txn = st.checkbox('Include Financial Transaction', value=True)
    t1, t2, t3 = st.columns(3)
    with t1:
        user_id = st.text_input('User ID', value='USER_1042')
        amount = st.number_input('Transaction Amount (₹)', value=85000.0, step=1000.0)
    with t2:
        txn_type = st.selectbox('Transaction Type', ['TRANSFER', 'PAYMENT', 'CASH_OUT', 'DEBIT'])
        device_id = st.text_input('Device ID', value='DEV_UNKNOWN_NEW_99')
    with t3:
        beneficiary_id = st.text_input('Beneficiary ID', value='BEN_UNKNOWN_MULE_1')
        location = st.text_input('Location', value='Lagos, NG')

    st.divider()
    submit = st.form_submit_button('🔀 Run Multi-Signal Risk Fusion Assessment', type='primary', use_container_width=True)

if submit:
    payload = {
        'session_id': f'session_{user_id}_{int(datetime.now().timestamp())}'
    }
    if include_msg and msg_text.strip():
        payload['message'] = msg_text.strip()
    if include_url and url_text.strip():
        payload['url'] = url_text.strip()
    if include_qr and qr_text.strip():
        payload['qr_payload'] = qr_text.strip()
    if include_txn:
        payload['transaction'] = {
            'user_id': user_id,
            'amount': float(amount),
            'transaction_type': txn_type,
            'device_id': device_id,
            'beneficiary_id': beneficiary_id,
            'location': location,
            'account_age_days': 180,
            'historical_avg_amount': 1500.0,
            'timestamp': datetime.now().isoformat()
        }

    with st.spinner('Fusing multi-signal vectors and evaluating scam chain logic...'):
        result = assess_risk_fusion(payload)

    if 'error' in result:
        st.error(f"Assessment failed: {result['error']}")
        st.stop()

    st.divider()
    st.subheader('🎯 Multi-Signal Risk Assessment Result')

    final_score = result.get('final_risk_score', 0)
    risk_level = result.get('risk_level', 'LOW')
    scam_chain = result.get('multi_stage_scam_chain_detected', False)
    is_critical = result.get('is_critical_threat', False)

    col1, col2, col3 = st.columns(3)
    with col1:
        risk_score_gauge(final_score, 'Fused Risk Score')
    with col2:
        st.metric('Overall Threat Level', risk_level)
        st.markdown(risk_badge(risk_level), unsafe_allow_html=True)
    with col3:
        st.metric('Scam Chain Escalation', '🚨 ESCALATED (≥85)' if scam_chain else 'NORMAL')

    if scam_chain:
        st.error('🔗 **MULTI-STAGE SCAM CHAIN DETECTED**: Phishing social engineering signal co-occurred with abnormal high-risk transaction. Threat score escalated by policy to CRITICAL.')
    elif risk_level == 'HIGH':
        st.error('🚨 **HIGH RISK**: Severe risk signals detected across submitted threat vectors.')
    elif risk_level == 'MEDIUM':
        st.warning('⚠️ **MEDIUM RISK**: Moderate suspicious indicators present.')
    else:
        st.success('✅ **LOW RISK**: Combined risk signals within safe operating thresholds.')

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader('📊 Component Signal Breakdown')
        comps = result.get('component_scores', [])
        for c in comps:
            name = c.get('name', '').replace('_', ' ').title()
            raw = c.get('raw_score', 0)
            wt = c.get('weight', 0)
            status = c.get('status', '')
            icon = '🔴' if raw >= 70 else ('🟡' if raw >= 40 else '🟢')
            st.markdown(f"{icon} **{name}**: `{raw:.1f}/100` *(Weight: {wt:.2f}, Status: {status})*")

        with st.expander('🔍 Risk Reasons', expanded=True):
            for r in result.get('summary_reasons', []):
                st.markdown(f'• {r}')

    with col_b:
        st.subheader('🛡️ Prescriptive Safety Actions')
        for i, a in enumerate(result.get('recommended_actions', [])):
            st.markdown(f'**{i+1}.** {a}')

    st.caption(f"Assessment ID: `{result.get('assessment_id', 'N/A')}` | Models: `{result.get('model_versions', {})}`")
"""

with open('frontend/pages/09_Model_Performance.py', 'w', encoding='utf-8') as f:
    f.write(p9)
with open('frontend/pages/11_Risk_Fusion.py', 'w', encoding='utf-8') as f:
    f.write(p11)

print('Updated 09 and 11 successfully')
