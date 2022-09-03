import secrets
from typing import Any, Optional

from pydantic import BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PASSWORD_RESET_TOKEN_EXPIRES_HOURS: int = 48

    PRIMARY_SUPERUSER_EMAIL: EmailStr
    PRIMARY_SUPERUSER_PHONE: str
    PRIMARY_SUPERUSER_PASSWORD: str
    PRIMARY_SUPERUSER_NAME: str

    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def build_db_connection_str(
        cls, v: Optional[str], values: Optional[dict[str, Any]]
    ) -> Any:
        if isinstance(v, str):
            return v
        else:
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_HOST"),
                port=values.get("POSTGRES_PORT"),
                path="/" + values.get("POSTGRES_DB") or ""
            )

    class Config:
        case_sensitive = True


settings = Settings()
