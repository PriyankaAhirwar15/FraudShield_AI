from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.alert import FraudAlertResponse, AlertUpdate
from app.services.alert_service import alert_service

router = APIRouter(prefix="/alerts", tags=["Fraud Alerts & Response"])

@router.get("", response_model=List[FraudAlertResponse])
def get_alerts(
    limit: int = Query(default=50, ge=1, le=200),
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return alert_service.list_alerts(db, limit=limit, status=status)

@router.patch("/{alert_id}", response_model=FraudAlertResponse)
def update_alert(alert_id: str, update_data: AlertUpdate, db: Session = Depends(get_db)):
    alert = alert_service.update_alert_status(db, alert_id, update_data.status)
    if not alert:
        raise HTTPException(status_code=404, detail="Fraud alert not found")
    return alert
