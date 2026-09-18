import sys, os
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
