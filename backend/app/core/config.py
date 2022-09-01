import secrets
from typing import Any, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PASSWORD_RESET_TOKEN_EXPIRES_HOURS = 48
    SECRET_KEY = secrets.token_urlsafe(32)
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
                scheme="postgresql",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_HOST"),
                port=values.get("POSTGRES_PORT"),
                path=values.get(f'/{"POSTGRES_DB"}' or ""),
            )

    class Config:
        case_sensitive = True


settings = Settings()
