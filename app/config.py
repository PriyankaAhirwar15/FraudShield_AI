import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FraudShield AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "dev_secret_key_fraudshield_ai_change_in_prod_2026"
    API_KEY: str = "fraudshield_secure_api_key_2026"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./fraudshield.db")
    
    # Risk Thresholds
    RISK_THRESHOLD_LOW: float = 40.0
    RISK_THRESHOLD_HIGH: float = 70.0
    
    # Risk Fusion Weights (Must sum to 1.0)
    WEIGHT_TRANSACTION: float = 0.35
    WEIGHT_BEHAVIOR: float = 0.25
    WEIGHT_URL: float = 0.20
    WEIGHT_MESSAGE: float = 0.15
    WEIGHT_QR: float = 0.05
    
    # Model Artifact Paths
    MODEL_DIR: str = "ml/saved_models"
    MODEL_REGISTRY_PATH: str = "ml/saved_models/model_registry.json"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
