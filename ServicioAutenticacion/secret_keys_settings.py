from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AUTHJWT_SECRET_KEY: str
    
    # Habilitar la denylist
    AUTHJWT_DENYLIST_ENABLED: bool = True
    
    AUTHJWT_DENYLIST_TOKEN_CHECKS: set = {"access", "refresh"}

    DB_PASSWORD: str
    DB_HOST: str
    DB_USER: str

    class Config:
        env_file = ".env"

settings = Settings()