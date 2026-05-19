from pathlib import Path
from pydantic import BaseSettings, Field, PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "SenAI CRM"
    environment: str = Field(default="development", env="APP_ENV")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    database_url: str = Field(..., env="DATABASE_URL")
    ingest_route_prefix: str = "/api"
    streamer_default_delay_seconds: float = 1.0

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
