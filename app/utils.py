import re

def title_case_bullets(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    out = []
    for l in lines:
        l = re.sub(r"^[-*\u2022\s]+", "", l)
        out.append(l[0].upper() + l[1:] if l else l)
    return "\n".join(out)