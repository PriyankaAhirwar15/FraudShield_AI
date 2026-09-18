import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import streamlit as st
import io
import qrcode
from frontend.api_client import scan_qr
from frontend.components.kpi_card import risk_score_gauge, risk_badge

st.title("📷 QR / Image Scam Scanner")
st.caption("Upload QR codes or payment screenshots — decoded and analyzed for scam indicators")
st.divider()

def render_qr_result(result: dict):
    """Render QR scan results."""
    st.subheader("🎯 QR Scan Assessment")

    if not result.get("qr_detected", False):
        reasons = result.get("reasons", ["No QR code detected in image."])
        st.warning(f"⚠️ No QR code detected — {reasons[0]}")
        return

    risk_score = result.get("qr_risk_score", 0)
    risk_level  = result.get("risk_level", "LOW")

    col1, col2, col3 = st.columns(3)
    with col1:
        risk_score_gauge(risk_score, "QR Risk Score")
    with col2:
        st.metric("Payload Type", result.get("payload_type", "UNKNOWN"))
        st.markdown(risk_badge(risk_level), unsafe_allow_html=True)
    with col3:
        st.metric("Risk Level", risk_level)

    if risk_level == "HIGH":
        st.error("🚨 HIGH RISK QR CODE — Do NOT approve this payment or click this link!")
    elif risk_level == "MEDIUM":
        st.warning("⚠️ MEDIUM RISK — Verify the beneficiary before approving any payment.")
    else:
        st.success("✅ LOW RISK — QR payload appears standard. Always verify recipient details.")

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        with st.expander("📦 Extracted Payload Details", expanded=True):
            raw = result.get("raw_payload", "")
            if raw:
                st.code(raw[:200], language="text")
            details = result.get("extracted_details", {})
            for k, v in details.items():
                if v:
                    st.write(f"**{k.replace('_',' ').title()}:** `{v}`")

    with col_b:
        with st.expander("🛡️ Risk Reasons & Recommendations", expanded=True):
            reasons = result.get("reasons", [])
            for r in reasons:
                icon = "✅" if "standard" in r.lower() else "🔴"
                st.markdown(f"{icon} {r}")
            st.divider()
            for i, act in enumerate(result.get("recommended_action", [])):
                st.markdown(f"**{i+1}.** {act}")

    st.caption(f"Scan ID: `{result.get('scan_id', 'N/A')}`")


# ── Tabs ─────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📁 Upload Image", "🧪 Generate Test QR"])

with tab1:
    uploaded_file = st.file_uploader(
        "Upload QR Code Image or Screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        help="Analyzed server-side — no embedded URL is visited"
    )
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        st.divider()
        scan_btn = st.button("🔍 Scan Image", type="primary", use_container_width=True)
        if scan_btn:
            with st.spinner("Decoding QR code and analyzing payload..."):
                result = scan_qr(uploaded_file.read(), uploaded_file.name)
            if "error" in result:
                st.error(f"Scan failed: {result['error']}")
            else:
                render_qr_result(result)

with tab2:
    st.subheader("Generate Test QR Code")
    col1, col2 = st.columns(2)
    with col1:
        qr_type = st.selectbox("Payload Type", ["UPI (High Risk)", "Phishing URL", "Crypto Address", "Safe URL"])
    with col2:
        custom_payload = st.text_input("Custom Payload (optional)")

    demo_payloads = {
        "UPI (High Risk)":  "upi://pay?pa=refund_support_kyc@upi&pn=Tax+Refund+Desk&am=25000",
        "Phishing URL":     "http://secure-login-sbi-kyc-update.xyz/auth/login",
        "Crypto Address":   "bitcoin:1A1zP1eP5QGefi2DMPTfTL5SLmv7Divfna",
        "Safe URL":         "https://www.hdfcbank.com"
    }
    payload_str = custom_payload or demo_payloads[qr_type]

    if st.button("Generate & Scan", type="primary", use_container_width=True):
        qr = qrcode.QRCode(version=1, box_size=6, border=3)
        qr.add_data(payload_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        img_bytes = buf.getvalue()

        col_img, col_res = st.columns([1, 2])
        with col_img:
            st.image(img_bytes, caption=f"Generated: {qr_type}", width=220)
        with col_res:
            with st.spinner("Analyzing generated QR code..."):
                result = scan_qr(img_bytes, "test_qr.png")
            if "error" in result:
                st.error(f"Scan failed: {result['error']}")
            else:
                render_qr_result(result)
