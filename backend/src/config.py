from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Determine the project base directory
PROJECT_BASE = Path(__file__).parent.parent.parent
ENV_LOCATION = PROJECT_BASE / ".env"

# Load environment variables from .env file
load_dotenv(ENV_LOCATION, override=True)

class ProjectSettings(BaseSettings):
    # API token for external service
    COIN_API_TOKEN: str

    class Config:
        env_file = str(ENV_LOCATION)
        env_file_encoding = 'utf-8'
        case_sensitive = True

# Create a global settings instance
project_settings = ProjectSettings()