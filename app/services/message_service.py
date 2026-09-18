import os
from app.config import settings
from app.core.logging import logger
from app.utils.helpers import calculate_risk_level, generate_id
from ml.common import load_artifact
from ml.phishing_message.preprocessor import clean_text, analyze_message_patterns

class MessageService:
    def __init__(self):
        self.model_path = os.path.join(settings.MODEL_DIR, "message_phishing_model.joblib")
        self.pipeline_artifact = None
        self.pipeline = None
        self.version = "msg_phishing_v1"
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.pipeline_artifact = load_artifact(self.model_path)
                self.pipeline = self.pipeline_artifact["pipeline"]
                self.version = self.pipeline_artifact.get("version", "msg_phishing_v1")
                logger.info("Loaded message phishing pipeline")
        except Exception as e:
            logger.error(f"Error loading message model: {e}")

    def analyze_message(self, message: str, channel: str = "SMS") -> dict:
        msg_id = generate_id("MSG")
        text_clean = clean_text(message)
        analysis = analyze_message_patterns(message)
        
        phish_prob = 0.05
        if self.pipeline is not None:
            try:
                probs = self.pipeline.predict_proba([text_clean])[0]
                phish_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception as e:
                logger.warning(f"NLP classification fallback: {e}")
                phish_prob = 0.5
                
        # Heuristic calibration
        if analysis["urgency_detected"] and analysis["credential_harvesting_detected"]:
            phish_prob = max(phish_prob, 0.88)
        elif analysis["impersonation_detected"] and len(analysis["extracted_urls"]) > 0:
            phish_prob = max(phish_prob, 0.82)
            
        risk_score = round(float(phish_prob * 100.0), 1)
        risk_level = calculate_risk_level(risk_score, settings.RISK_THRESHOLD_LOW, settings.RISK_THRESHOLD_HIGH)
        
        reasons = list(analysis["detected_indicators"])
        if not reasons:
            reasons.append("Message does not exhibit known social engineering or phishing patterns.")
            
        actions = []
        if risk_level == "HIGH":
            actions.append("Do NOT click any links or call phone numbers mentioned in this message.")
            actions.append("Banks never ask for OTPs, CVV, or passwords over SMS, Email, or WhatsApp.")
            actions.append("Forward this SMS to official telecom/cyber fraud reporting number (1930 / Chakshu).")
        elif risk_level == "MEDIUM":
            actions.append("Verify the sender ID and inspect any embedded links cautiously.")
            actions.append("Access services exclusively through official mobile apps or verified URLs.")
        else:
            actions.append("Message appears benign. Never share confidential financial credentials.")
            
        return {
            "message_id": msg_id,
            "phishing_risk_score": risk_score,
            "risk_level": risk_level,
            "is_phishing": bool(risk_score >= settings.RISK_THRESHOLD_LOW),
            "detected_indicators": analysis["detected_indicators"],
            "extracted_urls": analysis["extracted_urls"],
            "urgency_detected": analysis["urgency_detected"],
            "threat_detected": analysis["urgency_detected"],
            "impersonation_detected": analysis["impersonation_detected"],
            "reasons": reasons,
            "recommended_action": actions,
            "model_version": self.version
        }

message_service = MessageService()
