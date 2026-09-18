import re
import math
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "secure", "account", "update", "verify", "banking", "login", "signin",
    "password", "auth", "confirm", "wallet", "crypto", "free", "bonus",
    "kyc", "aadhaar", "pan", "otp", "support", "service", "payment",
    "claim", "refund", "suspend", "reward", "lottery", "gift", "unblock"
]

SUSPICIOUS_TLDS = [
    ".xyz", ".top", ".club", ".work", ".click", ".loan", ".men", ".fit",
    ".gq", ".cf", ".ga", ".ml", ".tk", ".buzz", ".monster", ".icu"
]

URL_FEATURE_COLUMNS = [
    "url_length",
    "domain_length",
    "num_dots",
    "num_hyphens",
    "num_underscores",
    "num_slashes",
    "num_question_marks",
    "num_equal_signs",
    "num_at_symbols",
    "num_subdomains",
    "is_https",
    "has_ip_address",
    "suspicious_keyword_count",
    "suspicious_tld",
    "entropy",
    "digit_ratio",
    "has_shortener"
]

def calculate_entropy(text: str) -> float:
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return -sum(p * math.log2(p) for p in prob)

def extract_url_features(url_str: str) -> dict:
    if not url_str:
        return {col: 0 for col in URL_FEATURE_COLUMNS}
        
    raw = url_str.strip()
    if not re.match(r"^https?://", raw, re.IGNORECASE):
        raw = "http://" + raw
        
    try:
        parsed = urlparse(raw)
        domain = parsed.netloc.lower()
        path = parsed.path
    except Exception:
        domain = raw.split("/")[0].lower()
        path = ""
        
    domain_clean = domain.split(":")[0]
    
    is_https = 1 if parsed.scheme == "https" else 0
    has_ip = 1 if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain_clean) else 0
    num_dots = domain_clean.count(".")
    num_subdomains = max(0, num_dots - 1) if not has_ip else 0
    
    full_url_lower = url_str.lower()
    kw_count = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in full_url_lower)
    
    has_suspicious_tld = 1 if any(domain_clean.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0
    
    shorteners = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly", "cutt.ly"]
    has_shortener = 1 if any(s in domain_clean for s in shorteners) else 0
    
    digits = sum(c.isdigit() for c in raw)
    digit_ratio = digits / max(len(raw), 1)
    
    feats = {
        "url_length": len(raw),
        "domain_length": len(domain_clean),
        "num_dots": num_dots,
        "num_hyphens": raw.count("-"),
        "num_underscores": raw.count("_"),
        "num_slashes": raw.count("/"),
        "num_question_marks": raw.count("?"),
        "num_equal_signs": raw.count("="),
        "num_at_symbols": raw.count("@"),
        "num_subdomains": num_subdomains,
        "is_https": is_https,
        "has_ip_address": has_ip,
        "suspicious_keyword_count": kw_count,
        "suspicious_tld": has_suspicious_tld,
        "entropy": round(calculate_entropy(raw), 3),
        "digit_ratio": round(digit_ratio, 3),
        "has_shortener": has_shortener
    }
    return feats

def detect_url_indicators(url_str: str, feats: dict) -> list:
    indicators = []
    if feats["has_ip_address"]:
        indicators.append("URL uses a raw IP address instead of a trusted domain name")
    if feats["is_https"] == 0:
        indicators.append("URL lacks SSL/HTTPS encryption (unsecured plaintext connection)")
    if feats["suspicious_keyword_count"] >= 2:
        indicators.append(f"Contains {feats['suspicious_keyword_count']} sensitive security/financial keywords")
    if feats["num_subdomains"] >= 3:
        indicators.append(f"Excessive subdomain nesting ({feats['num_subdomains']} subdomains) camouflaging fake hostnames")
    if feats["has_shortener"]:
        indicators.append("Uses a URL shortening service masking the actual destination host")
    if feats["suspicious_tld"]:
        indicators.append("Registered on a high-risk suspicious top-level domain (TLD)")
    if feats["num_at_symbols"] > 0:
        indicators.append("Contains '@' symbol which can redirect browser credentials")
    if feats["num_hyphens"] >= 3:
        indicators.append("Excessive hyphenation in domain/path mimicking legitimate brand names")
    return indicators
