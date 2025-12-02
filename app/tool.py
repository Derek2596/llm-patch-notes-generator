import httpx
from .config import cfg

async def fetch_current_date() -> str:
    """Fetch current UTC date from worldtimeapi. Returns ISO date string or raises."""
    url = cfg.WORLD_TIME_API
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get(url)
        r.raise_for_status()
        data = r.json()
        # example: datetime: "2025-12-01T12:34:56.789012+00:00"
        return data.get("datetime")