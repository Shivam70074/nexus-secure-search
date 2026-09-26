import re
from typing import Tuple

HONEYPOT_TOKENS = ["canary_admin_token", "honeypot_vip_user"]
PROMPT_INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"act as root",
    r"reveal system prompt",
    r"system prompt",
    r"bypass",
]
SENSITIVE_FIELDS = ["email", "phone", "attendance", "rsvp", "password", "ssn"]

class AINativeWAF:
    def inspect_query(self, query: str) -> Tuple[bool, int, str]:
        query_lower = query.lower()
        
        # Honeypot check
        for token in HONEYPOT_TOKENS:
            if token in query_lower:
                return False, 100, f"Honeypot token triggered: {token}"
                
        # SQL Injection check
        if "union" in query_lower or "select" in query_lower or "' or '1'='1" in query_lower:
            return False, 95, "SQL Injection attempt detected"

        # Prompt Injection check
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, query_lower):
                return False, 90, "Prompt injection attack detected"
                
        # Sensitive Data Exfiltration check
        for field in SENSITIVE_FIELDS:
            if field in query_lower:
                return False, 85, f"Sensitive data exfiltration attempt: {field}"
            
        return True, 0, "Query is safe"

waf = AINativeWAF()
