from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENV: str = "development"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutes
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    ACCESS_TOKEN_EXPIRE_SECONDS: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60
    REFRESH_TOKEN_EXPIRE_SECONDS: int = REFRESH_TOKEN_EXPIRE_MINUTES * 60

    COOKIES_SAMESITE: Literal["lax", "none", "strict"] = "lax" if ENV == "prod" else "lax"
    COOKIES_SECURE: bool = True if ENV == "prod" else False

    LIMIT_MAX: int = 100

    ROOT_PATH: Path = Path(__file__).parent.parent.resolve()

    POSTGRES_DB: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DRIVER: str = "asyncpg"

    POSTGRES_URL: str = (
        f"postgresql+{POSTGRES_DRIVER}"
        f"://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}"
        f"/{POSTGRES_DB}"
    )

    FIRST_USER_USERNAME: str = "admin"
    FIRST_USER_NAME: str = "Admin"
    FIRST_USER_PASSWORD: str = "123qweasdzxc"


settings = Settings()
