from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    GROQ_API_KEY: str
    ALLOW_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
