from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_URL: str
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "supersecret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str

    class Config:
        env_file = ".env"


settings = Settings()
