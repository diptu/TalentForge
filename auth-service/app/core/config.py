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


class Settings(BaseSettings):
    """Main application settings."""

    app_name: str = Field(..., alias="APP_NAME")
    env: str = Field(..., alias="ENV")
    debug: bool = Field(..., alias="DEBUG")
    port: int = Field(..., alias="PORT")

    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


# Singleton instance
settings = Settings()
