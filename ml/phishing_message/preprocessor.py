import re

URGENCY_PATTERNS = [
    r"\b(immediately|urgent|right now|today|within \d+ hours|24 hours|expires|suspended|blocked)\b",
    r"\b(action required|final notice|alert|warning|threat|emergency)\b"
]

IMPERSONATION_PATTERNS = [
    r"\b(sbi|hdfc|icici|axis|rbi|bank|income tax|kyc|pan card|aadhaar|paypal|amazon|netflix|paytm)\b",
    r"\b(customer care|security department|fraud department|support team)\b"
]

CREDENTIAL_HARVESTING_PATTERNS = [
    r"\b(click|link|verify|update|login|enter otp|enter pin|password|cvv|credentials|claim)\b",
    r"\b(apk|download|install|refund|lottery|prize|reward|cashback)\b"
]

def clean_text(text: str) -> str:
    if not text:
        return ""
    t = text.lower().strip()
    t = re.sub(r"\s+", " ", t)
    return t

def extract_urls_from_text(text: str) -> list:
    if not text:
        return []
    url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[^\s]*"
    urls = re.findall(url_pattern, text)
    return urls

def analyze_message_patterns(text: str) -> dict:
    t = clean_text(text)
    
    urgency = any(re.search(p, t, re.IGNORECASE) for p in URGENCY_PATTERNS)
    impersonation = any(re.search(p, t, re.IGNORECASE) for p in IMPERSONATION_PATTERNS)
    credential = any(re.search(p, t, re.IGNORECASE) for p in CREDENTIAL_HARVESTING_PATTERNS)
    urls = extract_urls_from_text(text)
    
    detected_indicators = []
    if urgency:
        detected_indicators.append("Urgency & psychological pressure tactics detected ('Immediate Action', 'Account Suspension')")
    if impersonation:
        detected_indicators.append("Financial institution or authority brand impersonation detected")
    if credential:
        detected_indicators.append("Call-to-action requesting credentials, OTP/PIN entry, or unverified link clicks")
    if len(urls) > 0:
        detected_indicators.append(f"Embedded hyperlinks detected ({len(urls)} link(s))")
        
    return {
        "urgency_detected": urgency,
        "impersonation_detected": impersonation,
        "credential_harvesting_detected": credential,
        "extracted_urls": urls,
        "detected_indicators": detected_indicators
    }
