from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./environments/.env.dev")

    MODE: Literal["DEV", "TEST", "PROD"] = "DEV"
    VISIBILITY_DOCUMENTATION: bool = False
    WEB_APP_URL: str = "http://localhost:3000"
    
    DB_HOST: str = "localhost"
    DB_NAME: str = "dev_db_tcard"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
