import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """
    Manages application settings, primarily Streamtape API credentials.
    """
    from typing import Optional

    STREAMTAPE_LOGIN: Optional[str] = os.getenv("STREAMTAPE_LOGIN")
    STREAMTAPE_KEY: Optional[str] = os.getenv("STREAMTAPE_KEY")
    STREAMTAPE_BASE_URL: str = "https://api.streamtape.com"

    def __init__(self):
        # Validate that credentials are set
        if not self.STREAMTAPE_LOGIN or not self.STREAMTAPE_KEY:
            raise ValueError(
                "Streamtape API credentials (STREAMTAPE_LOGIN and STREAMTAPE_KEY) "
                "must be set as environment variables in the .env file."
            )

settings = Settings()