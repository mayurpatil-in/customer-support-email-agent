from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "Customer Support Email Agent"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | str = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # OpenAI settings
    OPENAI_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")

settings = Settings()
