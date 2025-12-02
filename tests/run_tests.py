import json
import requests
import re

URL = "http://127.0.0.1:8000/generate"

def check_section_has_bullet(text: str, section: str) -> bool:
    """
    Returns True if the given section (Added/Changed/Removed) has at least one bullet.
    """
    # Define pattern for the next possible section header or end of string
    next_section_pattern = r"(?:Added:|Changed:|Removed:|$)"
    
    # Regex to capture content (group 1) of the current section up to the next header (lookahead)
    # The flags re.DOTALL and re.MULTILINE are essential for multi-line content
    pattern = rf"^{section}:\s*(.*?)(?={next_section_pattern})"
    
    # Search for the section content
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL | re.MULTILINE)
    
    if not match:
        return False
        
    # Extract the captured content and strip leading/trailing whitespace
    content = match.group(1).strip()
    
    # Check if the content has at least one line starting with '-' (a bullet point)
    return bool(re.search(r"^-", content, flags=re.MULTILINE))

def run_test(test_input, expected):
    response = requests.post(URL, json={"bullets": test_input, "style": "concise", "version": "Test"})
    if response.status_code != 200:
        return False, f"HTTP {response.status_code}"

    text = response.json().get("patch_notes", "")

    ok = True
    messages = []

    for section, should_have_bullet in expected.items():
        has_bullet = check_section_has_bullet(text, section)
        if has_bullet != should_have_bullet:
            ok = False
            messages.append(f"{section}: expected {should_have_bullet}, got {has_bullet}")

    return ok, "; ".join(messages) if messages else "OK"

def main():
    with open("tests/tests.json", "r") as f:
        tests = json.load(f)

    passed = 0
    failed = 0

    print("Running tests...\n")

    for i, test in enumerate(tests, 1):
        result, message = run_test(test["input"], test["expect"])
        if result:
            passed += 1
            print(f"Test {i}: PASS")
        else:
            failed += 1
            print(f"Test {i}: FAIL — {message}")

    print("\nSummary:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {len(tests)}")

if __name__ == "__main__":
    main()
