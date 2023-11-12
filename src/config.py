from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "LMS API"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
