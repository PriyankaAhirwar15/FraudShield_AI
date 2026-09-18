from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(64), unique=True, index=True, nullable=False)
    account_age = Column(Integer, default=30)
    avg_transaction_amount = Column(Float, default=1500.0)
    std_transaction_amount = Column(Float, default=500.0)
    normal_start_hour = Column(Integer, default=8)
    normal_end_hour = Column(Integer, default=22)
    created_at = Column(DateTime, default=utc_now)

    transactions = relationship("Transaction", back_populates="user")
    devices = relationship("Device", back_populates="user")
    beneficiaries = relationship("Beneficiary", back_populates="user")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), index=True, nullable=False)
    user_id = Column(String(64), ForeignKey("users.user_id"), index=True, nullable=False)
    device_type = Column(String(32), default="mobile")
    first_seen = Column(DateTime, default=utc_now)
    last_seen = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="devices")

class Beneficiary(Base):
    __tablename__ = "beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    beneficiary_id = Column(String(64), index=True, nullable=False)
    user_id = Column(String(64), ForeignKey("users.user_id"), index=True, nullable=False)
    name = Column(String(128), default="Beneficiary")
    transaction_count = Column(Integer, default=1)
    first_seen = Column(DateTime, default=utc_now)
    last_seen = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="beneficiaries")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(String(64), ForeignKey("users.user_id"), index=True, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(32), default="TRANSFER")
    merchant = Column(String(128), nullable=True)
    location = Column(String(64), default="Mumbai, IN")
    device_id = Column(String(64), nullable=False)
    beneficiary_id = Column(String(64), nullable=True)
    timestamp = Column(DateTime, default=utc_now)
    
    fraud_score = Column(Float, default=0.0)
    behavior_score = Column(Float, default=0.0)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String(16), default="LOW")
    reasons = Column(JSON, default=list)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="transactions")

class URLScan(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(String(64), unique=True, index=True, nullable=False)
    url = Column(String(512), nullable=False)
    domain = Column(String(256), nullable=True)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String(16), default="LOW")
    indicators = Column(JSON, default=list)
    reasons = Column(JSON, default=list)
    scan_timestamp = Column(DateTime, default=utc_now)

class MessageScan(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(64), unique=True, index=True, nullable=False)
    message_text_hash = Column(String(64), index=True, nullable=False)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String(16), default="LOW")
    detected_indicators = Column(JSON, default=list)
    extracted_urls = Column(JSON, default=list)
    reasons = Column(JSON, default=list)
    scan_timestamp = Column(DateTime, default=utc_now)

class QRScan(Base):
    __tablename__ = "qr_scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String(64), unique=True, index=True, nullable=False)
    extracted_content_hash = Column(String(64), index=True, nullable=False)
    payload_type = Column(String(32), default="TEXT")
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String(16), default="LOW")
    extracted_details = Column(JSON, default=dict)
    reasons = Column(JSON, default=list)
    scan_timestamp = Column(DateTime, default=utc_now)

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(64), unique=True, index=True, nullable=False)
    event_type = Column(String(32), index=True, nullable=False)
    event_id = Column(String(64), index=True, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(16), nullable=False)
    reasons = Column(JSON, default=list)
    recommended_action = Column(JSON, default=list)
    status = Column(String(32), default="NEW")
    created_at = Column(DateTime, default=utc_now)

class ModelPrediction(Base):
    __tablename__ = "model_predictions"

    id = Column(Integer, primary_key=True, index=True)
    prediction_id = Column(String(64), unique=True, index=True, nullable=False)
    model_name = Column(String(64), index=True, nullable=False)
    model_version = Column(String(32), nullable=False)
    input_reference = Column(String(64), nullable=True)
    prediction = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=utc_now)
