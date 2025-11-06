from pydantic import BaseSettings

class Settings(BaseSettings):
    AUTHJWT_SECRET_KEY: str

    DB_PASSWORD: str
    DB_HOST: str
    DB_USER: str

    class Config:
        env_file = ".env"

settings = Settings()