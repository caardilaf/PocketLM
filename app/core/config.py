from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "PocketLM API"
    version: str = "0.1.0"
    max_concurrent_requests: int = Field(default=4, ge=1)
    acquire_timeout_seconds: float = Field(default=0.0, ge=0)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
