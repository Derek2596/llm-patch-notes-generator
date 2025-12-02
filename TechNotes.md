# Technical Note: LLM Patch Notes Generator

**Goal:** Build an application using the Gemini API to transform unstructured development bullet points into formatted, categorized patch notes.

**Tool Use:** An external API call is used to fetch the current UTC date, which is then fed to the LLM for inclusion in the patch notes.

### 1. Architecture Diagram
The application uses a structure where the FastAPI service manages all requests, business logic, safety checks, and telemetry logging before interacting with the external APIs.
```
|--- CLIENT (index.html @ /ui) ---|
               | POST /generate
               v
|--- FASTAPI (main.py) ---|
| 1. Safety Checks: Injection/Length Guards
| 2. Telemetry: Log Start Time
| 3. Tool Use: Async Call to WorldTimeAPI
| 4. LLM Call (llm.py):
|    - System Prompt (prompts.py)
|    - User Prompt + Date Tool Data
|    - Calls Gemini API (gemini-2.5-flash)
| 5. Telemetry: Log Latency, Status
|--- GEMINI API ---|  <-- Returns Structured Patch Notes
        |
        v
|--- FASTAPI ---|
| 6. Return: {patch_notes: ..., meta: {...}}
        |
        v
|--- CLIENT ---|
```

### 2. Guardrails and Safety
| Guardrail                | Implementation                                                                                                                                    | Purpose                                                                              |
|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Input Length Guard       | Check in main.py and safety.py. Limits user input to 2,000 characters.                                                                            | Prevents excessive token consumption and API cost overruns.                          |
| Prompt Injection Check   | Function check_prompt_injection in safety.py uses regex against a blocklist (e.g., "ignore previous instructions").                               | Enforces the system prompt and prevents unauthorized behavior modification.          |
| System Prompt (Do/Don't) | Defined in prompts.py. Explicitly enforces output format (Version:, Added:, Changed:, Removed: in exact order) and semantic classification rules. | Guarantees structured, machine-parsable output for downstream usage (e.g., testing). |
| Error Fallback           | HTTPException (400, 413, 500) raised in main.py for safety violations or API failure.                                                             | Provides a graceful failure path and clear messaging to the user/client.             |

### 3. Evaluation Method
Offline Evaluation is performed using the run_test.py script against 15 test cases defined in tests.json.

**Method:** The script sends input to the live /generate endpoint. It then uses a robust regular expression with a positive lookahead in check_section_has_bullet to isolate the content of the Added:, Changed:, and Removed: sections.

**Metric:** Pass/Fail rate is determined by comparing the boolean output (Does the section have at least one bullet point?) against the expect dictionary in the test JSON. This verifies the LLM's classification and formatting adherence.

### 4. Known Limits
**Token/Cost Logging:** The current synchronous implementation of the Gemini API call (asyncio.to_thread) does not easily capture token usage directly from the response object within the main.py logic, leading to the tokens=-1 telemetry placeholder.