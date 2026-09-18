from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.analytics import AnalyticsOverview
from app.services.analytics_service import analytics_service

router = APIRouter(prefix="/analytics", tags=["Fraud Analytics"])

@router.get("/overview", response_model=AnalyticsOverview)
def get_analytics_overview(db: Session = Depends(get_db)):
    return analytics_service.get_overview(db)
