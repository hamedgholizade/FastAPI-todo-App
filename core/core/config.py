from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict
)


class Settings(BaseSettings):
    SQLARCHEMY_DATABASE_URL_POSTGRES: str
    
    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()
