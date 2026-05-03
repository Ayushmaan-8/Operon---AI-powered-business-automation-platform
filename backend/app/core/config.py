from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/operon"
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()