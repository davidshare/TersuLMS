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
    JWT_SECRET_KEY: str = "0adsdareewrweadfasgasopnnpooiqerqasga0alapopeqpsdgsdfhsdsdhfdstrgvfdsdhnbsgs"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_SECRET_KEY: str = "a3f67b124efb91c5d8e276f3b4a56c9b2d1e840f7b5a3086e0fd2c39e98d557f"
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
