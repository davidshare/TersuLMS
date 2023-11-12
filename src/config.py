from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "LMS API"
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="postgres"
    POSTGRES_DATABASE="lmsdb"
    POSTGRES_PORT="5432"
    POSTGRES_HOST="127.0.0.1"
    POSTGRES_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
