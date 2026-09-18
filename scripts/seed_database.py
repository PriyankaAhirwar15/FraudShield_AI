import os
import sys
sys.path.insert(0, ".")
import random
from datetime import datetime, timedelta
import pandas as pd

from app.database.session import SessionLocal, engine, Base
from app.database.models import User, Device, Beneficiary, Transaction, URLScan, MessageScan, QRScan, FraudAlert
from app.core.security import hash_sensitive_identifier
from app.utils.helpers import generate_id

def seed_database():
    print("Initializing tables and seeding database...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if already seeded
    if db.query(User).count() > 10:
        print("Database already contains seeded users and records. Skipping seed.")
        db.close()
        return

    # Seed 50 Users with varied baselines
    users_data = []
    base_time = datetime.utcnow() - timedelta(days=90)
    
    cities = ["Mumbai, IN", "Delhi, IN", "Bengaluru, IN", "Hyderabad, IN", "Chennai, IN", "Pune, IN"]
    merchants = ["Amazon Retail", "Flipkart Pay", "Swiggy", "Zomato", "Uber Rides", "Netflix India", "MakeMyTrip", "D-Mart", "CryptoEx Global", "Unknown Vendor"]
    
    print("Seeding Users, Devices, Beneficiaries...")
    for i in range(1, 51):
        u_id = f"USER_{1000 + i}"
        avg_amt = round(random.uniform(1000, 8000), 2)
        std_amt = round(avg_amt * random.uniform(0.15, 0.35), 2)
        
        user = User(
            user_id=u_id,
            account_age=random.randint(60, 1800),
            avg_transaction_amount=avg_amt,
            std_transaction_amount=std_amt,
            normal_start_hour=random.choice([7, 8, 9]),
            normal_end_hour=random.choice([21, 22, 23]),
            created_at=base_time
        )
        db.add(user)
        
        # Primary & Secondary Devices
        d1 = Device(device_id=f"DEV_{u_id}_PRIM", user_id=u_id, device_type="mobile", first_seen=base_time)
        d2 = Device(device_id=f"DEV_{u_id}_LAP", user_id=u_id, device_type="laptop", first_seen=base_time)
        db.add_all([d1, d2])
        
        # 3 to 6 Known Beneficiaries
        for j in range(1, random.randint(4, 7)):
            b = Beneficiary(
                beneficiary_id=f"BEN_{u_id}_{j}",
                user_id=u_id,
                name=f"Beneficiary {j} of {u_id}",
                transaction_count=random.randint(3, 25),
                first_seen=base_time
            )
            db.add(b)
            
    db.commit()
    print("Seeded 50 Users with Devices & Beneficiaries.")
    
    # Seed 300 historical transactions (including low, medium, and high risk)
    print("Seeding Historical Transactions & Alerts...")
    all_users = db.query(User).all()
    
    for k in range(300):
        u = random.choice(all_users)
        is_fraud_event = random.random() < 0.12 # 12% fraud alerts
        
        days_ago = random.randint(0, 89)
        hours_ago = random.randint(0, 23)
        tx_time = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
        
        if is_fraud_event:
            amt = round(u.avg_transaction_amount * random.uniform(5.0, 16.0), 2)
            dev_id = f"DEV_UNKNOWN_{random.randint(100, 999)}"
            ben_id = f"BEN_MULE_{random.randint(100, 999)}"
            risk_sc = round(random.uniform(78.0, 98.5), 1)
            risk_lv = "HIGH"
            fraud_sc = round(risk_sc / 100.0, 3)
            beh_sc = round(random.uniform(0.75, 0.95), 3)
            reasons = [
                f"Amount (Rs {amt:,.2f}) is {amt/u.avg_transaction_amount:.1f}x higher than user historical baseline",
                "Transaction initiated from an unrecognized hardware device ID",
                "Beneficiary account has no prior transaction history with user",
                "Transaction initiated outside customer regular business hours"
            ]
            actions = [
                "Temporary freeze placed on outgoing transfers",
                "OTP verification escalated to biometric authorization",
                "Incident routed to 24/7 Security Operations Center (SOC)"
            ]
        else:
            amt = round(max(50.0, random.gauss(u.avg_transaction_amount, u.std_transaction_amount)), 2)
            dev_id = f"DEV_{u.user_id}_PRIM"
            ben_id = f"BEN_{u.user_id}_1"
            risk_sc = round(random.uniform(5.0, 32.0), 1)
            risk_lv = "LOW"
            fraud_sc = round(risk_sc / 100.0, 3)
            beh_sc = 0.05
            reasons = ["Transaction pattern consistent with verified customer profile."]
            actions = ["Standard transaction safety."]
            
        txn_id = generate_id("TXN")
        tx = Transaction(
            transaction_id=txn_id,
            user_id=u.user_id,
            amount=amt,
            transaction_type=random.choice(["TRANSFER", "PAYMENT", "CASH_OUT", "DEBIT"]),
            merchant=random.choice(merchants),
            location=random.choice(cities),
            device_id=dev_id,
            beneficiary_id=ben_id,
            timestamp=tx_time,
            fraud_score=fraud_sc,
            behavior_score=beh_sc,
            risk_score=risk_sc,
            risk_level=risk_lv,
            reasons=reasons,
            created_at=tx_time
        )
        db.add(tx)
        
        if is_fraud_event or risk_sc >= 40.0:
            alert = FraudAlert(
                alert_id=generate_id("ALT"),
                event_type="TRANSACTION_FRAUD",
                event_id=txn_id,
                risk_score=risk_sc,
                risk_level=risk_lv,
                reasons=reasons,
                recommended_action=actions,
                status=random.choice(["NEW", "UNDER_INVESTIGATION", "RESOLVED_BLOCKED"]),
                created_at=tx_time
            )
            db.add(alert)
            
    # Seed historical URL scans
    urls_to_seed = [
        ("http://secure-login-hdfc-kyc-update.xyz/verify", 94.5, "HIGH", ["Raw suspicious TLD (.xyz)", "Multiple financial keywords ('secure', 'login', 'kyc', 'update')"]),
        ("http://192.168.1.105/sbi-online-portal/login.php", 91.0, "HIGH", ["Raw IP address destination host", "Impersonation of SBI banking brand"]),
        ("https://www.hdfcbank.com/personal/ways-to-bank/online-banking", 4.2, "LOW", ["Trusted SSL certificate and official domain"]),
        ("http://bit.ly/claim-tax-refund-immediate", 82.0, "HIGH", ["URL shortener masking destination", "Urgency refund trigger words"])
    ]
    for u_str, sc, lv, r_list in urls_to_seed:
        scan = URLScan(
            url_id=generate_id("URL"),
            url=u_str,
            domain=u_str.split("/")[2] if "/" in u_str else u_str,
            risk_score=sc,
            risk_level=lv,
            indicators=r_list,
            reasons=r_list,
            scan_timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 48))
        )
        db.add(scan)
        
    db.commit()
    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
