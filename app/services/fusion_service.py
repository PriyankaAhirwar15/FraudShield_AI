from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from app.config import settings
from app.utils.helpers import calculate_risk_level, generate_id
from app.services.fraud_service import fraud_service
from app.services.behavior_service import behavior_service
from app.services.url_service import url_service
from app.services.message_service import message_service
from app.database.models import FraudAlert, Transaction, URLScan, MessageScan

class FusionService:
    def __init__(self):
        self.default_weights = {
            "transaction": settings.WEIGHT_TRANSACTION,
            "behavior": settings.WEIGHT_BEHAVIOR,
            "url": settings.WEIGHT_URL,
            "message": settings.WEIGHT_MESSAGE,
            "qr": settings.WEIGHT_QR
        }

    def assess_multi_signal(
        self,
        db: Session,
        transaction_data: Optional[dict] = None,
        url_text: Optional[str] = None,
        message_text: Optional[str] = None,
        qr_payload: Optional[str] = None,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> dict:
        assessment_id = generate_id("ASSESS")
        weights = custom_weights or self.default_weights
        
        scores_breakdown = []
        all_reasons = []
        factor_attributions = []
        
        tx_score = 0.0
        beh_score = 0.0
        url_score = 0.0
        msg_score = 0.0
        qr_score = 0.0
        
        is_url_flagged = False
        is_msg_flagged = False
        is_tx_flagged = False
        is_beh_flagged = False
        
        # 1. Message Analysis
        if message_text:
            msg_res = message_service.analyze_message(message_text)
            msg_score = msg_res["phishing_risk_score"]
            is_msg_flagged = msg_score >= settings.RISK_THRESHOLD_LOW
            all_reasons.extend([f"[Message Signal] {r}" for r in msg_res["reasons"] if "benign" not in r.lower()])
            
            # If message contained URLs, auto-scan first URL
            if msg_res["extracted_urls"] and not url_text:
                url_text = msg_res["extracted_urls"][0]
                
        # 2. URL Analysis
        if url_text:
            url_res = url_service.scan_url(url_text)
            url_score = url_res["url_risk_score"]
            is_url_flagged = url_score >= settings.RISK_THRESHOLD_LOW
            all_reasons.extend([f"[URL Signal] {r}" for r in url_res["reasons"] if "No common" not in r])
            
        # 3. QR Payload
        if qr_payload:
            # Basic analysis of text payload
            if "upi://" in qr_payload or "http" in qr_payload:
                qr_score = 65.0
                all_reasons.append(f"[QR Signal] Direct payment intent or web link embedded in QR payload.")
            else:
                qr_score = 20.0
                
        # 4. Behavioral & Transaction Fraud
        if transaction_data:
            user_id = transaction_data.get("user_id", "USER_DEFAULT")
            amt = float(transaction_data.get("amount", 1000.0))
            dev_id = transaction_data.get("device_id", "DEV_DEFAULT")
            ben_id = transaction_data.get("beneficiary_id")
            loc = transaction_data.get("location", "Mumbai, IN")
            
            # Behavioral Profile
            beh_res = behavior_service.analyze_behavior(
                db=db,
                user_id=user_id,
                amount=amt,
                device_id=dev_id,
                beneficiary_id=ben_id,
                location=loc,
                timestamp=transaction_data.get("timestamp")
            )
            beh_score = float(beh_res["behavior_anomaly_score"] * 100.0)
            is_beh_flagged = beh_score >= settings.RISK_THRESHOLD_LOW
            all_reasons.extend([f"[Behavioral Anomaly] {r}" for r in beh_res["reasons"]])
            
            # Transaction Fraud Model
            tx_res = fraud_service.predict_transaction(
                amount=amt,
                transaction_type=transaction_data.get("transaction_type", "TRANSFER"),
                user_id=user_id,
                transaction_id=transaction_data.get("transaction_id"),
                timestamp=transaction_data.get("timestamp"),
                location=loc,
                device_id=dev_id,
                beneficiary_id=ben_id,
                account_age=transaction_data.get("account_age_days", 180),
                historical_avg=beh_res["profile_metrics"]["avg_amount"],
                historical_std=beh_res["profile_metrics"]["std_amount"],
                is_new_device=beh_res["is_new_device"],
                is_new_beneficiary=beh_res["is_new_beneficiary"]
            )
            tx_score = tx_res["risk_score"]
            is_tx_flagged = tx_score >= settings.RISK_THRESHOLD_LOW
            all_reasons.extend([f"[Transaction ML] {r}" for r in tx_res["reasons"] if "align with" not in r])
            if tx_res.get("contributing_factors"):
                factor_attributions = tx_res["contributing_factors"]
                
        # 5. Multi-Signal Weighting & Active Inputs Normalization
        active_signals = []
        if transaction_data:
            active_signals.extend([("transaction", tx_score), ("behavior", beh_score)])
        if url_text:
            active_signals.append(("url", url_score))
        if message_text:
            active_signals.append(("message", msg_score))
        if qr_payload:
            active_signals.append(("qr", qr_score))
            
        if not active_signals:
            active_signals = [("transaction", 10.0)]
            
        total_active_weight = sum(weights.get(k, 0.2) for k, _ in active_signals)
        total_active_weight = max(total_active_weight, 0.01)
        
        fused_score = 0.0
        for name, sc in active_signals:
            w = weights.get(name, 0.2)
            normalized_w = w / total_active_weight
            weighted_sc = sc * normalized_w
            fused_score += weighted_sc
            scores_breakdown.append({
                "name": name.replace("_", " ").title(),
                "raw_score": round(sc, 1),
                "weight": round(normalized_w, 3),
                "weighted_score": round(weighted_sc, 1),
                "status": "HIGH_RISK" if sc >= 70 else ("MEDIUM_RISK" if sc >= 40 else "NORMAL")
            })
            
        # 6. Multi-Stage Scam Chain Escalation Logic
        # If user received phishing msg/URL AND attempted high anomaly transaction -> High correlation penalty
        multi_stage_chain = False
        if (is_msg_flagged or is_url_flagged) and (is_tx_flagged or is_beh_flagged):
            multi_stage_chain = True
            fused_score = max(fused_score + 18.0, 85.0)
            all_reasons.insert(0, "[CRITICAL SCAM CORRELATION] Multi-stage social-engineering attack detected: Phishing lure linked to suspicious financial transfer execution.")
            
        final_risk_score = round(float(min(max(fused_score, 0.0), 100.0)), 1)
        risk_level = calculate_risk_level(final_risk_score, settings.RISK_THRESHOLD_LOW, settings.RISK_THRESHOLD_HIGH)
        
        # Recommendations
        actions = []
        if risk_level == "HIGH":
            actions.append("HALT TRANSACTION: Do not enter OTP, UPI PIN, or bank passwords.")
            actions.append("Do not click links or install any software (.APK/screen sharing) requested by third parties.")
            actions.append("Contact official bank fraud helpline immediately to place a temporary block on the account.")
        elif risk_level == "MEDIUM":
            actions.append("Verify recipient details via an independent, trusted communication channel.")
            actions.append("Confirm that the website address is correct and secured with HTTPS.")
        else:
            actions.append("Standard security precautions: keep passwords and OTPs private.")
            
        if not all_reasons:
            all_reasons = ["All monitored risk signals are within normal safe tolerances."]
            
        # 7. Record Fraud Alert in DB if HIGH or MEDIUM risk
        if final_risk_score >= settings.RISK_THRESHOLD_LOW:
            alert = FraudAlert(
                alert_id=generate_id("ALT"),
                event_type="MULTI_SIGNAL_FUSION" if len(active_signals) > 1 else active_signals[0][0].upper(),
                event_id=assessment_id,
                risk_score=final_risk_score,
                risk_level=risk_level,
                reasons=all_reasons[:6],
                recommended_action=actions,
                status="NEW"
            )
            db.add(alert)
            db.commit()
            
        return {
            "assessment_id": assessment_id,
            "final_risk_score": final_risk_score,
            "risk_level": risk_level,
            "is_critical_threat": bool(final_risk_score >= settings.RISK_THRESHOLD_HIGH),
            "multi_stage_scam_chain_detected": multi_stage_chain,
            "component_scores": scores_breakdown,
            "summary_reasons": all_reasons,
            "factor_attributions": factor_attributions,
            "recommended_actions": actions,
            "model_versions": {
                "transaction_model": fraud_service.version,
                "behavior_model": "behavior_iforest_v1",
                "url_model": url_service.version,
                "message_model": message_service.version
            }
        }

fusion_service = FusionService()
