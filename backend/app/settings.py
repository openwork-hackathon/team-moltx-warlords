from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Backend runtime settings.

    All fields can be set via environment variables.
    """

    model_config = SettingsConfigDict(env_prefix="", extra="ignore")

    ENV: str = "dev"  # dev|staging|prod
    CORS_ORIGINS: str = ""  # comma-separated list (e.g. http://localhost:5173)

    # Database
    # Default: local sqlite file for dev. Swap to Postgres/Supabase by setting DATABASE_URL.
    DATABASE_URL: str = "sqlite:///./app.db"

    @property
    def cors_origins(self) -> list[str]:
        if not self.CORS_ORIGINS.strip():
            return []
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
