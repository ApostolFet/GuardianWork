import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    bot_token: str


def get_db_uri():
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    return f"postgresql://{user}:{password}@{host}/{db_name}"
