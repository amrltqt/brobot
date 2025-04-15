from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Brobot learning API"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./database.db"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
