import os
from datetime import datetime
import pandas as pd
import numpy as np

from app.config import settings
from app.core.logging import logger
from app.utils.helpers import calculate_risk_level, generate_id
from ml.common import load_artifact
from ml.transaction_fraud.features import extract_single_transaction_features, TRANSACTION_FEATURE_COLUMNS

class FraudService:
    def __init__(self):
        self.model_path = os.path.join(settings.MODEL_DIR, "transaction_fraud_model.joblib")
        self.explainer_path = os.path.join(settings.MODEL_DIR, "transaction_shap_explainer.joblib")
        self.model_artifact = None
        self.model = None
        self.explainer = None
        self.version = "fraud_model_v1"
        self._load_models()

    def _load_models(self):
        try:
            if os.path.exists(self.model_path):
                self.model_artifact = load_artifact(self.model_path)
                self.model = self.model_artifact["model"]
                self.version = self.model_artifact.get("version", "fraud_model_v1")
                logger.info(f"Loaded transaction fraud model ({self.version})")
            if os.path.exists(self.explainer_path):
                self.explainer = load_artifact(self.explainer_path)
                logger.info("Loaded transaction SHAP explainer")
        except Exception as e:
            logger.error(f"Error loading fraud model artifacts: {e}")

    def predict_transaction(
        self,
        amount: float,
        transaction_type: str = "TRANSFER",
        user_id: str = "USER_DEFAULT",
        transaction_id: str = None,
        timestamp: datetime = None,
        location: str = "Mumbai, IN",
        device_id: str = "DEV_PRIMARY",
        beneficiary_id: str = None,
        account_age: int = 180,
        historical_avg: float = 1500.0,
        historical_std: float = 500.0,
        is_new_device: bool = False,
        is_new_beneficiary: bool = False,
        velocity_1h: float = 1.0,
        velocity_24h: float = 2.0,
        location_score: float = 0.0
    ) -> dict:
        txn_id = transaction_id or generate_id("TXN")
        ts = timestamp or datetime.now()
        
        # 1. Feature Engineering
        feats_df = extract_single_transaction_features(
            amount=amount,
            txn_type=transaction_type,
            timestamp=ts,
            account_age=account_age,
            historical_avg=historical_avg,
            historical_std=historical_std,
            velocity_1h=velocity_1h,
            velocity_24h=velocity_24h,
            is_new_device=is_new_device,
            is_new_beneficiary=is_new_beneficiary,
            location_score=location_score
        )
        
        # 2. Model Prediction
        fraud_prob = 0.05
        if self.model is not None:
            try:
                probs = self.model.predict_proba(feats_df)[0]
                fraud_prob = float(probs[1]) if len(probs) > 1 else float(probs[0])
            except Exception as e:
                logger.warning(f"Fallback probability: {e}")
                fraud_prob = 0.5
                
        # Heuristic calibration for high deviations / novel device + beneficiary combinations
        amount_ratio = amount / max(historical_avg, 1.0)
        if amount_ratio > 8.0 and (is_new_device or is_new_beneficiary):
            fraud_prob = max(fraud_prob, 0.88)
        elif amount_ratio > 4.0 and is_new_device and is_new_beneficiary:
            fraud_prob = max(fraud_prob, 0.92)
        elif amount_ratio > 3.0:
            fraud_prob = max(fraud_prob, 0.65)
            
        # 3. SHAP Explainability
        factors = []
        if self.explainer is not None:
            factors = self.explainer.explain_instance(feats_df)
            
        # 4. Generate human-readable reasons
        reasons = []
        if amount_ratio >= 3.0:
            reasons.append(f"Transaction amount (₹{amount:,.2f}) is {amount_ratio:.1f}x above the user's historical average (₹{historical_avg:,.2f}).")
        if is_new_device:
            reasons.append(f"Transaction initiated from an unrecognized device hardware identifier ({device_id}).")
        if is_new_beneficiary:
            reasons.append("Beneficiary has no verified transaction history with this account.")
        if feats_df["is_night_hour"].iloc[0] == 1:
            reasons.append(f"Transaction occurs at an unusual night hour ({ts.strftime('%H:%M')}).")
        if velocity_1h >= 3:
            reasons.append(f"High velocity surge: {int(velocity_1h)} transactions within the last 60 minutes.")
        if location_score > 0.6:
            reasons.append(f"Originating IP location ({location}) indicates significant distance from regular activity center.")
            
        if not reasons:
            reasons.append("Transaction characteristics align with established behavioral patterns.")
            
        # 5. Prescriptive safety recommendations
        actions = []
        risk_score = round(fraud_prob * 100.0, 1)
        risk_level = calculate_risk_level(risk_score, settings.RISK_THRESHOLD_LOW, settings.RISK_THRESHOLD_HIGH)
        
        if risk_level == "HIGH":
            actions.append("Do NOT share or enter OTP, UPI PIN, or NetBanking password.")
            actions.append("Independently verify beneficiary credentials before releasing funds.")
            actions.append("If this payment was not initiated by you, immediately freeze card/account via official bank helpline.")
        elif risk_level == "MEDIUM":
            actions.append("Double-check the recipient name and account number.")
            actions.append("Ensure you are on the official bank portal or app.")
        else:
            actions.append("Standard transaction safety rules apply. Keep login credentials confidential.")
            
        return {
            "transaction_id": txn_id,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "fraud_probability": round(fraud_prob, 4),
            "is_fraud": bool(fraud_prob >= 0.5),
            "reasons": reasons,
            "contributing_factors": factors,
            "recommended_action": actions,
            "model_version": self.version
        }

fraud_service = FraudService()
