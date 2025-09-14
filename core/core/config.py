from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SQLARCHEMY_DATABASE_URL_POSTGRES: str
    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
