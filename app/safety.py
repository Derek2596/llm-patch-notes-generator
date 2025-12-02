import re
from .config import cfg

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"forget the above",
    r"disregard earlier",
]

def check_prompt_injection(text: str) -> bool:
    t = text.lower()
    for p in INJECTION_PATTERNS:
        if re.search(p, t):
            return True
        return False

def check_input_length(text: str, max_chars: int) -> bool:
    return len(text) <= max_chars