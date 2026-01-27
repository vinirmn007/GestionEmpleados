from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTHJWT_SECRET_KEY: str = "secret-key-123"

    class Config:
        case_sensitive = True

settings = Settings()
