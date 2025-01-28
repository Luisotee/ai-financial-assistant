from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "WL/UG Chatbot"
    PORT: int = 8000

    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None

    # Azure OpenAI Model Configuration
    AZURE_MODEL_NAME: str = "gpt-4o-mini"
    AZURE_MODEL_TEMPERATURE: float = 0.7

    # Search Configuration
    SERPER_API_KEY: Optional[str] = None

    # Google Sheets Configuration
    GOOGLE_ACCOUNT_FILE: str = "credentials/credentials.json"
    GOOGLE_SPREADSHEET_ID: Optional[str] = None

    # Groq Configuration
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"
    GROQ_MODEL_TEMPERATURE: float = 0.7

    # Model Selection
    MODEL_PROVIDER: str = "azure"  # "azure" or "groq"

    def validate_api_keys(self):
        # Get the base project directory (2 levels up from config.py)
        base_dir = Path(__file__).parent.parent.parent.parent
        creds_path = base_dir / self.GOOGLE_ACCOUNT_FILE

        if self.MODEL_PROVIDER not in ["azure", "groq"]:
            raise ValueError("MODEL_PROVIDER must be either 'azure' or 'groq'")

        if self.MODEL_PROVIDER == "azure":
            if not self.AZURE_OPENAI_API_KEY:
                raise ValueError("AZURE_OPENAI_API_KEY is required for Azure")
            if not self.AZURE_OPENAI_ENDPOINT:
                raise ValueError("AZURE_OPENAI_ENDPOINT is required for Azure")
        elif self.MODEL_PROVIDER == "groq":
            if not self.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY is required for Groq")

        if not self.SERPER_API_KEY:
            raise ValueError("SERPER_API_KEY is required")
        if not self.GOOGLE_SPREADSHEET_ID:
            raise ValueError("GOOGLE_SPREADSHEET_ID is required")
        if not creds_path.exists():
            raise ValueError(
                f"Google credentials file not found at {creds_path}"
            )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Initialize settings
settings = Settings()
