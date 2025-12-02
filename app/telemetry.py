import logging
import time
from pathlib import Path

LOG_PATH = Path("logs/requests.log")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(message)s')

def record_request(timestamp: float, pathway: str, latency_ms: float, input_len: int, tokens: int | None = None):
    ts = int(timestamp)
    tokens = tokens or -1
    logging.info(f"{ts},pathway={pathway},latency_ms={latency_ms:.1f},input_len={input_len},tokens={tokens}")