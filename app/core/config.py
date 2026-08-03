from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    TEST_DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    PROJECT_NAME: str = "E-Commerce Backend API"
    API_VERSION: str = "v1"
    DEBUG: bool = False
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    MAIL_FROM_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int


settings = Settings()
