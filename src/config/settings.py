from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "LMS API"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DATABASE: str = "lmsdb"
    POSTGRES_PORT: str = "5432"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    HASH_ALGORITHM: str = "eqeer"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
