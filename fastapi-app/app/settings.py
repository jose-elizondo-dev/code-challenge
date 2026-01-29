from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    api_token: str  # Secret token for API authentication

    # Pydantic Settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",      # Load from .env file
        env_prefix="",        # No prefix for env variables
        case_sensitive=False,  # Case-insensitive env variable names
    )


# Singleton instance of settings
settings = Settings()
