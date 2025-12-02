from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"
    TEMPERATURE: float = 0.2
    WORLD_TIME_API: str = "http://worldtimeapi.org/api/timezone/Etc/UTC"
    MAX_INPUT_CHARS: int = 2000

    class Config:
        env_file = ".env"

cfg = Settings()