from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    GOOGLE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
