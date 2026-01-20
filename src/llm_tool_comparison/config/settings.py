"""Application settings using Pydantic."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(env_file='.env', case_sensitive=False)

    # LangFuse settings
    langfuse_public_key: str
    langfuse_secret_key: str
    langfuse_base_url: str = "https://cloud.langfuse.com"
    langfuse_enabled: bool = True

    # API keys
    openai_api_key: str
    google_api_key: str

    # Judge settings
    judge_enabled: bool = True
    judge_model: str = "gpt-4.1"


settings = Settings()
