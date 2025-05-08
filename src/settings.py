from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_id: int
    api_hash: str
    bot_session_name: str = Field(default="tracker-bot")
    host: str = "0.0.0.0"
    port: int = 8000

    api_key: str = Field(default="")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
