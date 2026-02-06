
from pydantic.v1 import BaseSettings

class Settings(BaseSettings):
    AUTHJWT_SECRET_KEY: str = "alexisjosue12345"  # Default fallback, should be from env
    
    class Config:
        case_sensitive = True

settings = Settings()
