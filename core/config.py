import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str
    model_name: str
    eodhd_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None
    mistral_api_key: Optional[str] = None

    # 👇 Add this for consistent project-wide file I/O
    USER_WORKDIR: str = os.path.join(os.getcwd(), "user_workdir")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
