# app/core/config.py
"""Application settings using Pydantic Settings (async ready)."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """PostgreSQL async database configuration."""

    uri: str = Field(..., alias="DB_URI")
    pool_min: int = Field(10, alias="DB_POOL_MIN")
    pool_max: int = Field(50, alias="DB_POOL_MAX")
    replica1_host: str | None = Field(None, alias="DB_REPLICA1_HOST")
    replica2_host: str | None = Field(None, alias="DB_REPLICA2_HOST")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class RedisSettings(BaseSettings):
    """Redis configuration."""

    host: str = Field(..., alias="REDIS_HOST")
    port: int = Field(..., alias="REDIS_PORT")
    password: str = Field(..., alias="REDIS_PASSWORD")
    db: int = Field(..., alias="REDIS_DB")
    cache_ttl: int = Field(..., alias="REDIS_CACHE_TTL")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class JWTSettings(BaseSettings):
    """JWT authentication settings."""

    secret_key: str = Field(..., alias="JWT_SECRET_KEY")
    algorithm: str = Field(..., alias="JWT_ALGORITHM")
    access_expire_minutes: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_expire_days: int = Field(..., alias="REFRESH_TOKEN_EXPIRE_DAYS")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class RateLimitSettings(BaseSettings):
    """Rate limiting configuration."""

    count: int = Field(5, alias="RATE_LIMIT_COUNT")
    window: int = Field(60, alias="RATE_LIMIT_WINDOW")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class Settings(BaseSettings):
    """Main application settings."""

    app_name: str = Field(..., alias="APP_NAME")
    base_url: str = Field(..., alias="BASE_URL")
    env: str = Field(..., alias="ENV")
    debug: bool = Field(..., alias="DEBUG")
    port: int = Field(..., alias="PORT")

    database: DatabaseSettings = DatabaseSettings()  # type: ignore[call-arg]
    redis: RedisSettings = RedisSettings()  # type: ignore[call-arg]
    jwt: JWTSettings = JWTSettings()  # type: ignore[call-arg]
    rate_limit: RateLimitSettings = RateLimitSettings()  # type: ignore[call-arg]
    model_config = SettingsConfigDict(env_file=".env", extra="allow")


# Singleton instance
settings = Settings()  # type: ignore[call-arg]
