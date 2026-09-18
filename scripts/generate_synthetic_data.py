import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)

def generate_synthetic_transactions(n_samples=10000, fraud_ratio=0.035):
    set_seed(42)
    n_fraud = int(n_samples * fraud_ratio)
    n_legit = n_samples - n_fraud
    
    users = [f"USER_{1000 + i}" for i in range(250)]
    user_baselines = {
        u: {
            "avg_amt": np.random.uniform(800, 5000),
            "std_amt": np.random.uniform(200, 1200),
            "known_devices": [f"DEV_{u}_1", f"DEV_{u}_2"],
            "known_beneficiaries": [f"BEN_{u}_{j}" for j in range(random.randint(3, 10))]
        }
        for u in users
    }
    
    records = []
    base_time = datetime.now() - timedelta(days=90)
    
    # Legit transactions (including noisy edge cases like vacation travel, sudden high-value festive purchase)
    for i in range(n_legit):
        u = random.choice(users)
        b = user_baselines[u]
        
        # 5% of legit transactions are irregular (large purchase, travel, night purchase)
        is_irregular = random.random() < 0.05
        if is_irregular:
            amt = b["avg_amt"] * np.random.uniform(2.5, 4.5)
            hour = np.random.choice([22, 23, 0, 1, 7, 13])
            dev = f"DEV_NEW_{random.randint(1, 50)}" if random.random() < 0.3 else random.choice(b["known_devices"])
            ben = f"BEN_NEW_{random.randint(1, 50)}" if random.random() < 0.4 else random.choice(b["known_beneficiaries"])
            vel_1h = random.choice([1, 2, 3])
            vel_24h = random.randint(2, 6)
            loc_score = round(np.random.uniform(0.3, 0.7), 3)
        else:
            amt = max(50.0, np.random.normal(b["avg_amt"], b["std_amt"]))
            hour = np.random.choice(range(8, 22))
            dev = random.choice(b["known_devices"])
            ben = random.choice(b["known_beneficiaries"])
            vel_1h = 1
            vel_24h = random.randint(1, 3)
            loc_score = round(np.random.beta(1, 10), 3)
            
        txn_time = base_time + timedelta(days=random.randint(0, 89), hours=int(hour), minutes=random.randint(0, 59))
        
        records.append({
            "transaction_id": f"TXN_LEGIT_{i:06d}",
            "user_id": u,
            "amount": round(amt, 2),
            "historical_avg_amount": round(b["avg_amt"], 2),
            "historical_std_amount": round(b["std_amt"], 2),
            "transaction_type": random.choice(["PAYMENT", "TRANSFER", "DEBIT", "PAYMENT"]),
            "timestamp": txn_time.isoformat(),
            "hour": hour,
            "device_id": dev,
            "is_new_device": 1 if dev not in b["known_devices"] else 0,
            "beneficiary_id": ben,
            "is_new_beneficiary": 1 if ben not in b["known_beneficiaries"] else 0,
            "velocity_1h": vel_1h,
            "velocity_24h": vel_24h,
            "account_age_days": random.randint(60, 1500),
            "location_distance_score": loc_score,
            "is_fraud": 0
        })
        
    # Fraud transactions (including smart stealth low-amount testing frauds and massive drain frauds)
    for i in range(n_fraud):
        u = random.choice(users)
        b = user_baselines[u]
        
        is_stealth = random.random() < 0.15 # 15% stealth fraud
        if is_stealth:
            amt = b["avg_amt"] * np.random.uniform(1.2, 2.2)
            hour = np.random.choice([10, 14, 16, 20])
            vel_1h = random.randint(2, 4)
            vel_24h = random.randint(4, 9)
        else:
            amt = b["avg_amt"] * np.random.uniform(4.5, 20.0)
            hour = np.random.choice([1, 2, 3, 4, 5, 23, 0])
            vel_1h = random.randint(3, 9)
            vel_24h = random.randint(8, 22)
            
        txn_time = base_time + timedelta(days=random.randint(0, 89), hours=int(hour), minutes=random.randint(0, 59))
        dev = f"DEV_UNKNOWN_{random.randint(100, 999)}"
        ben = f"BEN_MULE_{random.randint(100, 999)}"
        
        records.append({
            "transaction_id": f"TXN_FRAUD_{i:06d}",
            "user_id": u,
            "amount": round(amt, 2),
            "historical_avg_amount": round(b["avg_amt"], 2),
            "historical_std_amount": round(b["std_amt"], 2),
            "transaction_type": random.choice(["TRANSFER", "CASH_OUT", "TRANSFER"]),
            "timestamp": txn_time.isoformat(),
            "hour": hour,
            "device_id": dev,
            "is_new_device": 1,
            "beneficiary_id": ben,
            "is_new_beneficiary": 1,
            "velocity_1h": vel_1h,
            "velocity_24h": vel_24h,
            "account_age_days": random.randint(5, 400),
            "location_distance_score": round(np.random.beta(6, 2), 3),
            "is_fraud": 1
        })
        
    df = pd.DataFrame(records).sample(frac=1.0, random_state=42).reset_index(drop=True)
    os.makedirs("data/synthetic", exist_ok=True)
    df.to_csv("data/synthetic/transactions.csv", index=False)
    print(f"Generated realistic transactions: {len(df)} rows ({n_fraud} fraud, {len(df)-n_fraud} legit)")
    return df

def generate_synthetic_urls(n_samples=4000):
    set_seed(42)
    legit_domains = [
        "google.com", "microsoft.com", "amazon.in", "hdfcbank.com", "icicibank.com",
        "sbi.co.in", "github.com", "stackoverflow.com", "linkedin.com", "netflix.com",
        "wikipedia.org", "apple.com", "nytimes.com", "flipkart.com", "zerodha.com",
        "paytm.com", "phonepe.com", "axisbank.com", "paypal.com", "stripe.com"
    ]
    legit_paths = [
        "login", "account/dashboard", "profile/settings", "help/center",
        "products/item/1209", "about-us", "terms-and-conditions", "contact",
        "security/settings", "verify/email", "support/tickets"
    ]
    
    phish_keywords = ["secure-login", "verify-kyc", "update-pan", "account-blocked", "free-reward", "claim-bonus", "unblock-bank", "wallet-refund"]
    phish_tlds = [".xyz", ".top", ".club", ".click", ".buzz", ".monster", ".work", ".cf", ".icu", ".online"]
    
    urls = []
    # 50% legit
    for i in range(n_samples // 2):
        d = random.choice(legit_domains)
        p = random.choice(legit_paths)
        scheme = "https://" if random.random() > 0.08 else "http://"
        urls.append({"url": f"{scheme}{d}/{p}", "label": 0})
        
    # 50% phishing (with subtle and overt variants)
    for i in range(n_samples // 2):
        ptype = random.choice(["subdomain_spoof", "ip_address", "keyword_tld", "shortener", "hyphen_brand", "typosquat"])
        if ptype == "subdomain_spoof":
            target = random.choice(["sbi", "hdfc", "icici", "paypal", "netflix", "paytm"])
            tld = random.choice(phish_tlds)
            u = f"http://secure-login.{target}.verify-portal{tld}/auth/login"
        elif ptype == "ip_address":
            ip = f"{random.randint(11, 210)}.{random.randint(10, 250)}.{random.randint(10, 250)}.{random.randint(1, 250)}"
            u = f"http://{ip}/banking/online/verify.php"
        elif ptype == "keyword_tld":
            kw = random.choice(phish_keywords)
            tld = random.choice(phish_tlds)
            u = f"http://{kw}-portal-service{tld}/index.html?token={random.randint(100000, 999999)}"
        elif ptype == "shortener":
            u = f"https://bit.ly/bank-kyc-urgent-{random.randint(10, 99)}"
        elif ptype == "typosquat":
            typo = random.choice(["hdfc-bank-security", "sbi-online-portal", "icici-customer-care", "axis-kyc-update"])
            u = f"https://www.{typo}.com/verify/index.php"
        else:
            target = random.choice(["hdfc-bank", "sbi-online", "icici-kyc", "axis-support"])
            u = f"http://www.{target}-verification-update.com/login"
        urls.append({"url": u, "label": 1})
        
    df = pd.DataFrame(urls).sample(frac=1.0, random_state=42).reset_index(drop=True)
    df.to_csv("data/synthetic/urls.csv", index=False)
    print(f"Generated realistic URLs: {len(df)} rows")
    return df

def generate_synthetic_messages(n_samples=3000):
    set_seed(42)
    legit_templates = [
        "Your OTP for payment of Rs {amt} is {otp}. Do not share this OTP with anyone.",
        "Dear customer, Rs {amt} credited to your account XX{acc} via NEFT from {sender}.",
        "Your electricity bill of Rs {amt} is due on {date}. Pay via official app.",
        "Welcome to our service. Your order #{order} has been shipped via BlueDart.",
        "Salary for the month has been processed and credited to your account XX{acc}.",
        "Reminder: Doctor appointment scheduled for tomorrow at 10:00 AM.",
        "Your statement for card ending XX{acc} is now ready to view on netbanking.",
        "Thank you for dining with us! Here is your e-receipt for Rs {amt}.",
        "Your flight ticket to Bengaluru is confirmed. PNR: {pnr}.",
        "Your subscription to Prime has renewed. Receipt sent to your registered email."
    ]
    
    phish_templates = [
        "Dear Customer, your {bank} account is suspended today due to pending KYC. Click http://bit.ly/bank-kyc-verify to update PAN immediately or account will be blocked.",
        "URGENT: Suspicious transaction of Rs {amt} detected on your account. If not you, cancel immediately at http://secure-bank-cancel-auth.xyz",
        "Congratulations! You won Rs 50,00,000 lottery from KBC / RBI. Claim your reward immediately by clicking http://claim-prize-bonus.top",
        "Income Tax Refund of Rs {amt} approved. Update bank account details now at http://192.168.1.10/refund/login to receive funds.",
        "Dear user, your SIM card will be deactivated in 24 hours. Update Aadhaar details urgently: http://sim-kyc-verify-portal.club",
        "Your electricity connection will be disconnected tonight at 9:30 PM. Call bill officer at 9876543210 or pay at http://elec-bill-pay.link",
        "Dear customer, your credit card points worth Rs {amt} are expiring today. Redeem for cash voucher now: http://reward-redeem-bank.click",
        "HDFC Alert: Your NetBanking password expired. Reset password immediately to avoid transaction block: http://hdfc-pass-reset.work",
        "SBI Notice: Unauthorized login from Lagos. If not you, secure account immediately at http://sbi-secure-portal.monster",
        "Dear customer, loan of Rs 5,00,000 pre-approved with zero interest. Click http://instant-loan-approval.xyz to disburse."
    ]
    
    data = []
    banks = ["SBI", "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Bank"]
    
    for i in range(n_samples // 2):
        t = random.choice(legit_templates).format(
            amt=random.randint(100, 5000),
            otp=random.randint(100000, 999999),
            acc=random.randint(10, 99),
            sender="Employer Ltd",
            date="25th Oct",
            order=random.randint(10000, 99999),
            pnr="PNR" + str(random.randint(1000, 9999))
        )
        data.append({"message": t, "label": 0})
        
    for i in range(n_samples // 2):
        t = random.choice(phish_templates).format(
            bank=random.choice(banks),
            amt=random.randint(15000, 95000)
        )
        data.append({"message": t, "label": 1})
        
    df = pd.DataFrame(data).sample(frac=1.0, random_state=42).reset_index(drop=True)
    df.to_csv("data/synthetic/messages.csv", index=False)
    print(f"Generated realistic messages: {len(df)} rows")
    return df

if __name__ == "__main__":
    generate_synthetic_transactions()
    generate_synthetic_urls()
    generate_synthetic_messages()
    print("All datasets generated.")
