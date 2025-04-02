import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    model_name: str
    eodhd_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    mistral_api_key: Optional[str] = None

    # Allow override via .env, fallback to ../../user_workdir
    USER_WORKDIR: str = os.getenv(
        "USER_WORKDIR",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "user_workdir"))
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()

# ✅ Auto-create working directory if it doesn't exist
os.makedirs(settings.USER_WORKDIR, exist_ok=True)
print(f"✅ USER_WORKDIR set to: {settings.USER_WORKDIR}")
