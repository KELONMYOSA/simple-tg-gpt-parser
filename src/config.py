from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    TG_API_ID: str
    TG_API_HASH: str

    OPENAI_API_KEY: str


settings = Settings()
