import os
from urllib.parse import urlparse
import pandas as pd

from app.config import settings
from app.core.logging import logger
from app.utils.helpers import calculate_risk_level
from ml.common import load_artifact
from ml.phishing_url.extractor import extract_url_features, detect_url_indicators, URL_FEATURE_COLUMNS

class URLService:
    def __init__(self):
        self.model_path = os.path.join(settings.MODEL_DIR, "url_phishing_model.joblib")
        self.model_artifact = None
        self.model = None
        self.version = "url_phishing_v1"
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model_artifact = load_artifact(self.model_path)
                self.model = self.model_artifact["model"]
                self.version = self.model_artifact.get("version", "url_phishing_v1")
                logger.info("Loaded URL Phishing model")
        except Exception as e:
            logger.error(f"Error loading URL model: {e}")

    def scan_url(self, url: str) -> dict:
        clean_url = url.strip()
        features = extract_url_features(clean_url)
        indicators = detect_url_indicators(clean_url, features)
        
        try:
            parsed = urlparse(clean_url if clean_url.startswith("http") else "http://" + clean_url)
            domain = parsed.netloc.lower()
        except Exception:
            domain = clean_url.split("/")[0].lower()
            
        # ML Inference
        phish_prob = 0.1
        if self.model is not None:
            try:
                df_feats = pd.DataFrame([features])[URL_FEATURE_COLUMNS]
                probs = self.model.predict_proba(df_feats)[0]
                phish_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception as e:
                logger.warning(f"URL inference note: {e}")
                phish_prob = 0.5
                
        # Heuristic boost
        if features["has_ip_address"] or features["suspicious_tld"]:
            phish_prob = max(phish_prob, 0.85)
        if features["suspicious_keyword_count"] >= 2:
            phish_prob = max(phish_prob, 0.78)
            
        risk_score = round(float(phish_prob * 100.0), 1)
        risk_level = calculate_risk_level(risk_score, settings.RISK_THRESHOLD_LOW, settings.RISK_THRESHOLD_HIGH)
        
        reasons = []
        if indicators:
            reasons.extend(indicators)
        else:
            reasons.append("No common lexical, structural, or heuristic phishing markers were detected.")
            
        actions = []
        if risk_level == "HIGH":
            actions.append("Do NOT open this link or enter banking credentials, passwords, or personal info.")
            actions.append("Report link to cyber security / bank fraud prevention team.")
            actions.append("Clear browser cache and run an antivirus scan if the link was previously opened.")
        elif risk_level == "MEDIUM":
            actions.append("Verify the exact domain spelling and ensure valid SSL certificate.")
            actions.append("Prefer navigating directly to official portal via bookmarks or search engine.")
        else:
            actions.append("Standard browsing safety applies. Ensure URL bar displays https://.")
            
        return {
            "url": clean_url,
            "domain": domain,
            "url_risk_score": risk_score,
            "risk_level": risk_level,
            "is_phishing": bool(risk_score >= settings.RISK_THRESHOLD_LOW),
            "detected_indicators": indicators,
            "reasons": reasons,
            "domain_characteristics": features,
            "recommended_action": actions,
            "model_version": self.version
        }

url_service = URLService()
