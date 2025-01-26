from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "WL/UG Chatbot"
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    SERPER_API_KEY: Optional[str] = None

    def validate_api_keys(self):
        if not self.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY is required")
        if not self.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT is required")
        if not self.SERPER_API_KEY:
            raise ValueError("SERPER_API_KEY is required")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"  # Allow extra fields in the settings


# Initialize settings
settings = Settings()
