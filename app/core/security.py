import hashlib
import re

def hash_sensitive_identifier(identifier: str, salt: str = "fraudshield_salt") -> str:
    if not identifier:
        return ""
    return hashlib.sha256(f"{salt}:{identifier}".encode("utf-8")).hexdigest()

def sanitize_phone_or_card(value: str) -> str:
    if not value:
        return ""
    clean = re.sub(r"\D", "", str(value))
    if len(clean) >= 12:
        return f"****-****-****-{clean[-4:]}"
    elif len(clean) >= 10:
        return f"******{clean[-4:]}"
    return f"***{clean[-2:]}" if len(clean) > 2 else "***"

def sanitize_log_message(msg: str) -> str:
    return re.sub(r"(?i)(otp|pin|cvv|password)\s*[:=]\s*(\w+)", r"\1: [REDACTED]", msg)
