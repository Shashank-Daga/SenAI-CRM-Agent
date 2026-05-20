from pathlib import Path
from pydantic import BaseSettings, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    app_name: str = "SenAI CRM"
    environment: str = Field(default="development", env="APP_ENV")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    database_url: str = Field(..., env="DATABASE_URL")
    ingest_route_prefix: str = "/api"
    streamer_default_delay_seconds: float = 1.0
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openrouter_api_key: str = Field(default="", env="OPENROUTER_API_KEY")
    llm_model: str = Field(default="gpt-4", env="LLM_MODEL")
    company_name: str = Field(default="SenAI", env="COMPANY_NAME")
    scrape_timeout_seconds: int = Field(default=10, env="SCRAPE_TIMEOUT_SECONDS")
    scrape_retry_count: int = Field(default=3, env="SCRAPE_RETRY_COUNT")
    intelligence_cache_ttl_hours: int = Field(default=6, env="INTELLIGENCE_CACHE_TTL_HOURS")

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
