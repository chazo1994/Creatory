import json
from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Creatory API"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "info"
    api_workers: int = Field(default=2, alias="API_WORKERS")

    api_prefix: str = "/api/v1"

    database_url: str = Field(
        default="postgresql+asyncpg://creatory:creatory@localhost:5432/creatory",
        alias="DATABASE_URL",
    )
    sql_echo: bool = False
    db_pool_size: int = Field(default=10, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, alias="DB_MAX_OVERFLOW")

    jwt_secret_key: str = Field(default="change-me-in-production", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    cors_origins: list[str] = Field(default_factory=list, alias="CORS_ORIGINS")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, list):
            return value
        if not value:
            return []

        value = value.strip()
        if value.startswith("["):
            loaded = json.loads(value)
            if not isinstance(loaded, list):
                raise ValueError("CORS_ORIGINS must be a list")
            return [str(item).strip() for item in loaded if str(item).strip()]

        return [item.strip() for item in value.split(",") if item.strip()]

    @model_validator(mode="after")
    def validate_production_settings(self) -> "Settings":
        if self.app_env.lower() != "production":
            return self

        weak_secrets = {
            "change-me-in-production",
            "replace-with-strong-secret",
            "replace-with-a-32-char-minimum-secret",
        }
        if len(self.jwt_secret_key) < 32 or self.jwt_secret_key in weak_secrets:
            raise ValueError("JWT_SECRET_KEY must be at least 32 chars in production")

        if "*" in self.cors_origins:
            raise ValueError("CORS_ORIGINS cannot contain '*' in production")

        return self


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
