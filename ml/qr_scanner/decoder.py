import cv2
import numpy as np
import io
import re
from urllib.parse import parse_qs, urlparse
from PIL import Image

class QRScanner:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def decode_image_bytes(self, image_bytes: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            open_cv_image = np.array(image)
            open_cv_image = open_cv_image[:, :, ::-1].copy()
        except Exception as e:
            return {
                "qr_detected": False,
                "error": f"Failed to decode image file: {str(e)}",
                "payload_type": "NONE",
                "raw_payload": "",
                "qr_risk_score": 0.0,
                "risk_level": "LOW",
                "is_suspicious": False,
                "reasons": ["Uploaded file is not a valid or readable image."]
            }
            
        val, pts, st_code = self.detector.detectAndDecode(open_cv_image)
        
        if not val:
            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            val, pts, st_code = self.detector.detectAndDecode(gray)
            
        if not val:
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray if 'gray' in locals() else cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY))
            val, pts, st_code = self.detector.detectAndDecode(enhanced)
            
        if not val:
            return {
                "qr_detected": False,
                "payload_type": "NONE",
                "raw_payload": "",
                "qr_risk_score": 10.0,
                "risk_level": "LOW",
                "extracted_details": {},
                "is_suspicious": False,
                "reasons": ["No standard QR code matrix was detected in the submitted image."]
            }
            
        raw_text = val.strip()
        parsed = self.parse_payload(raw_text)
        return parsed

    def parse_payload(self, text: str) -> dict:
        reasons = []
        extracted_details = {}
        risk_score = 15.0
        
        if text.startswith("upi://pay") or "upi://" in text:
            payload_type = "UPI"
            try:
                parsed_url = urlparse(text)
                params = parse_qs(parsed_url.query)
                pa = params.get("pa", [""])[0]
                pn = params.get("pn", [""])[0]
                am = params.get("am", [""])[0]
                
                extracted_details = {
                    "payee_vpa": pa,
                    "payee_name": pn,
                    "prefilled_amount": am,
                    "raw_uri": text
                }
                
                if not pa:
                    risk_score += 40.0
                    reasons.append("Malformed UPI QR code missing designated payee address (VPA)")
                if am and float(am) > 10000:
                    risk_score += 25.0
                    reasons.append(f"Pre-configured auto-debit amount is high (₹{float(am):,.2f})")
                if any(kw in (pa+pn).lower() for kw in ["refund", "cashback", "reward", "lottery", "support", "kyc"]):
                    risk_score += 45.0
                    reasons.append("UPI Payee VPA or Name uses deceptive refund/cashback keywords (Common reverse-payment scam)")
            except Exception:
                extracted_details = {"raw": text}
                
        elif re.match(r"^https?://", text, re.IGNORECASE):
            payload_type = "URL"
            extracted_details = {"destination_url": text}
            risk_score += 20.0
            reasons.append("QR code redirects to an external web URL")
            
        elif re.match(r"^(bitcoin:|ethereum:|bc1|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40})", text):
            payload_type = "CRYPTO"
            extracted_details = {"crypto_address": text}
            risk_score += 40.0
            reasons.append("QR code encodes an irreversible cryptocurrency wallet address")
            
        else:
            payload_type = "TEXT"
            extracted_details = {"text_content": text}
            
        risk_score = float(min(max(risk_score, 0.0), 100.0))
        risk_level = "HIGH" if risk_score >= 70 else ("MEDIUM" if risk_score >= 40 else "LOW")
        
        return {
            "qr_detected": True,
            "payload_type": payload_type,
            "raw_payload": text,
            "extracted_details": extracted_details,
            "qr_risk_score": round(risk_score, 1),
            "risk_level": risk_level,
            "is_suspicious": bool(risk_score >= 40),
            "reasons": reasons if reasons else ["QR code format and destination appear standard."]
        }
