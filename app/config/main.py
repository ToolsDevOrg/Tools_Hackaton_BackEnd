from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./environments/.env.dev")

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    VISIBILITY_DOCUMENTATION: bool = False
    WEB_APP_URL: str = "http://localhost:3000"
    UJIN_TOKEN: str

    DB_HOST: str = "localhost"
    DB_NAME: str = "dev_db"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    SECRET_KEY: str = "secret"
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
