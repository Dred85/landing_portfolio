from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Portfolio FastAPI"
    CONTACT_EMAIL: str = "adrolv@rambler.ru"

    class Config:
        env_file = ".env"

settings = Settings()
