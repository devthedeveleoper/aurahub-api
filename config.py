from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional, List, Union, Any

class Settings(BaseSettings):
    """
    Manages application settings, including Streamtape API credentials and CORS origins.
    """
    # Configure Pydantic to load environment variables from a .env file.
    # 'extra="ignore"' allows for other environment variables not explicitly defined here.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    STREAMTAPE_BASE_URL: str = "https://api.streamtape.com"
    STREAMTAPE_LOGIN: Optional[str] = None
    STREAMTAPE_KEY: Optional[str] = None

    # New setting for allowed CORS origins.
    # It will read a comma-separated string from .env.
    # Default to ["*"] if not specified, allowing all origins.
    ALLOWED_ORIGINS: Union[str, List[str]] = "*" # Temporarily accept str or list

    # Pydantic lifecycle method to perform validation/transformation after initial parsing.
    def model_post_init(self, __context: Any) -> None:
        # Ensure that STREAMTAPE_LOGIN and STREAMTAPE_KEY are set
        if not self.STREAMTAPE_LOGIN or not self.STREAMTAPE_KEY:
            raise ValueError(
                "Streamtape API credentials (STREAMTAPE_LOGIN and STREAMTAPE_KEY) "
                "must be set as environment variables in the .env file."
            )

        # Parse ALLOWED_ORIGINS string into a list if it's not already a list
        if isinstance(self.ALLOWED_ORIGINS, str):
            if self.ALLOWED_ORIGINS == "*":
                # If it's the wildcard string, keep it as is, or convert to ["*"]
                # For CORSMiddleware, "*" is directly accepted.
                self.ALLOWED_ORIGINS = ["*"]
            else:
                # Split by comma, strip whitespace from each origin
                self.ALLOWED_ORIGINS = [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]

settings = Settings()