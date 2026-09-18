from app.utils.helpers import generate_id
from ml.qr_scanner.decoder import QRScanner
from app.services.url_service import url_service

class QRService:
    def __init__(self):
        self.scanner = QRScanner()

    def process_image(self, image_bytes: bytes) -> dict:
        scan_id = generate_id("QR")
        res = self.scanner.decode_image_bytes(image_bytes)
        res["scan_id"] = scan_id
        
        # If QR contains a URL, correlate with URL scanner
        if res.get("payload_type") == "URL" and res.get("raw_payload"):
            url_res = url_service.scan_url(res["raw_payload"])
            res["qr_risk_score"] = max(res["qr_risk_score"], url_res["url_risk_score"])
            res["risk_level"] = url_res["risk_level"]
            res["is_suspicious"] = bool(res["qr_risk_score"] >= 40.0)
            res["reasons"].extend([f"Embedded URL Assessment: {r}" for r in url_res["reasons"]])
            res["recommended_action"] = url_res["recommended_action"]
        else:
            actions = []
            if res.get("risk_level") == "HIGH":
                actions.append("Do NOT scan or approve payment requests from unknown or suspicious QR codes.")
                actions.append("Remember: Scanning a QR code is ONLY for SENDING money, NEVER for receiving refunds/cashback.")
            elif res.get("risk_level") == "MEDIUM":
                actions.append("Carefully check the beneficiary name before confirming payment in your UPI app.")
            else:
                actions.append("Standard payment verification applies.")
            res["recommended_action"] = actions
            
        return res

qr_service = QRService()
