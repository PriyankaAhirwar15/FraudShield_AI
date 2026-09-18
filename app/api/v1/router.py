from fastapi import APIRouter
from app.api.v1.fraud import router as fraud_router
from app.api.v1.behavior import router as behavior_router
from app.api.v1.url import router as url_router
from app.api.v1.qr import router as qr_router
from app.api.v1.message import router as message_router
from app.api.v1.risk import router as risk_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.models import router as models_router
from app.api.v1.health import router as health_router

api_router = APIRouter()

api_router.include_router(fraud_router)
api_router.include_router(behavior_router)
api_router.include_router(url_router)
api_router.include_router(qr_router)
api_router.include_router(message_router)
api_router.include_router(risk_router)
api_router.include_router(alerts_router)
api_router.include_router(analytics_router)
api_router.include_router(models_router)
api_router.include_router(health_router)
