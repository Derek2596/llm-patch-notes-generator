from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pathlib import Path
from pydantic import BaseModel
import time
import uvicorn
from .llm import generate_patch_notes
from .tool import fetch_current_date
from .safety import check_prompt_injection, check_input_length
from .telemetry import record_request
from .config import cfg

app = FastAPI(title="Patch Note Generator")

class GenerateRequest(BaseModel):
    bullets: str
    style: str = "concise"
    version: str | None = None

@app.post("/generate")
async def generate(req: GenerateRequest, request: Request):
    # Basic input guards
    if check_prompt_injection(req.bullets):
        raise HTTPException(status_code=400, detail="Prompt injection detected and rejected.")
    if not check_input_length(req.bullets, cfg.MAX_INPUT_CHARS):
        raise HTTPException(status_code=413, detail=f"Input too long (max {cfg.MAX_INPUT_CHARS} chars)")

    start = time.time()
    # Tool: fetch date from external API
    try:
        date_str = await fetch_current_date()
        pathway = "tool"
    except Exception:
        date_str = None
        pathway = "none"

    try:
        result = await generate_patch_notes(bullets=req.bullets, style=req.style, version=req.version, date_str=date_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    latency = (time.time() - start) * 1000
    record_request(timestamp=start, pathway=pathway, latency_ms=latency, input_len=len(req.bullets))

    return {"patch_notes": result, "meta": {"pathway": pathway, "latency_ms": latency}}

@app.get("/")
def root_redirect():
    # Redirects the user to the UI path
    return RedirectResponse(url="/ui/")

static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)

app.mount(
    "/ui", 
    StaticFiles(directory=static_dir, html=True), 
    name="static"
)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)