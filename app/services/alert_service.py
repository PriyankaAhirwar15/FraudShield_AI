from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.models import FraudAlert
from app.utils.helpers import generate_id

class AlertService:
    def list_alerts(self, db: Session, limit: int = 50, status: Optional[str] = None) -> List[FraudAlert]:
        query = db.query(FraudAlert)
        if status:
            query = query.filter(FraudAlert.status == status)
        return query.order_by(desc(FraudAlert.created_at)).limit(limit).all()

    def get_alert_by_id(self, db: Session, alert_id: str) -> Optional[FraudAlert]:
        return db.query(FraudAlert).filter(FraudAlert.alert_id == alert_id).first()

    def update_alert_status(self, db: Session, alert_id: str, new_status: str) -> Optional[FraudAlert]:
        alert = self.get_alert_by_id(db, alert_id)
        if alert:
            alert.status = new_status
            db.commit()
            db.refresh(alert)
        return alert

    def create_alert(
        self,
        db: Session,
        event_type: str,
        event_id: str,
        risk_score: float,
        risk_level: str,
        reasons: list,
        recommended_action: list
    ) -> FraudAlert:
        alert = FraudAlert(
            alert_id=generate_id("ALT"),
            event_type=event_type,
            event_id=event_id,
            risk_score=risk_score,
            risk_level=risk_level,
            reasons=reasons,
            recommended_action=recommended_action,
            status="NEW"
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert

alert_service = AlertService()
