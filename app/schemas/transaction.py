from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class TransactionInput(BaseModel):
    transaction_id: Optional[str] = Field(default=None, description="Unique transaction ID")
    user_id: str = Field(..., description="Unique customer user ID")
    amount: float = Field(..., gt=0, description="Transaction amount in currency units")
    transaction_type: str = Field(default="TRANSFER", description="TRANSFER, PAYMENT, CASH_OUT, DEBIT")
    merchant: Optional[str] = Field(default=None, description="Merchant name or category")
    timestamp: Optional[datetime] = Field(default=None, description="Transaction ISO timestamp")
    location: str = Field(default="Mumbai, IN", description="Transaction location / IP geolocation")
    device_id: str = Field(..., description="Device identifier or fingerprint hash")
    beneficiary_id: Optional[str] = Field(default=None, description="Beneficiary account/ID")
    account_age_days: Optional[int] = Field(default=180, description="Account age in days")
    historical_avg_amount: Optional[float] = Field(default=1500.0, description="User historical avg amount")
    historical_txn_count: Optional[int] = Field(default=45, description="Historical txn count")

class TransactionPredictionResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    transaction_id: str
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: str
    fraud_probability: float = Field(..., ge=0, le=1)
    behavior_anomaly_score: float = Field(..., ge=0, le=1)
    is_fraud: bool
    reasons: List[str]
    contributing_factors: List[dict] = []
    recommended_action: List[str]
    model_version: str
