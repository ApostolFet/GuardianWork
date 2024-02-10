import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    bot_token: str


class DataBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="db_",
        extra="ignore",
    )
    host: str
    user: str
    password: str
    name: str


def get_db_uri():
    db_settings = DataBaseSettings()
    return f"postgresql://{db_settings.user}:{db_settings.password}@{db_settings.host}/{db_settings.name}"
