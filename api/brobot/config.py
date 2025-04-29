from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Brobot learning API"
    APP_VERSION: str = "1.0.0"
    DATABASE_URL: str
    MODEL_NAME: str

    class Config:
        case_sensitive = True


settings = Settings()
