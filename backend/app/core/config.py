from typing import Any, Optional

from pydantic import BaseSettings, EmailStr, PostgresDsn, validator


class Settings(BaseSettings):
    CLIENT_BASE_URL = "http://localhost:8000"
    API_V1: str = "/api/v1"
    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 48

    PRIMARY_SUPERUSER_EMAIL: EmailStr  # type: ignore
    PRIMARY_SUPERUSER_PHONE: str
    PRIMARY_SUPERUSER_PASSWORD: str
    INACTIVE_USER_EMAIL: EmailStr
    INACTIVE_USER_PASSWORD: str
    TEST_USER_EMAIL: EmailStr = "test@user.com"  # type: ignore
    TEST_USER_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def build_db_connection_str(
        cls, v: Optional[str], values: dict[str, Optional[str]]
    ) -> Optional[str]:
        if isinstance(v, str):
            return v
        else:
            return PostgresDsn.build(
                scheme="postgresql+asyncpg",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_HOST"),
                port=values.get("POSTGRES_PORT"),
                path=f'/{values.get("POSTGRES_DB", "")}',
            )
    GITHUB_CLIENT_ID: str
    GITHUB_SECRET_KEY: str
    GITHUB_REDIRECT_URI = f"{CLIENT_BASE_URL}{API_V1}/oauth2github"
    GITHUB_AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
    GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_API_ENDPOINT = "https://api.github.com/user"

    GOOGLE_CLIENT_ID: str
    GOOGLE_SECRET_KEY: str
    GOOGLE_REDIRECT_URI = f"{CLIENT_BASE_URL}{API_V1}/oauth2google"
    GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_ACCESS_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_API_ENDPOINT = "https://www.googleapis.com/auth/userinfo.email"
    class Config:
        case_sensitive = True


settings = Settings()
