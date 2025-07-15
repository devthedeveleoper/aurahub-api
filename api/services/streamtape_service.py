import httpx
from fastapi import HTTPException
from config import settings
from typing import Dict, Any, Optional

class StreamtapeService:
    """
    Service class to interact with the Streamtape API.
    Handles HTTP requests and common error responses.
    """
    def __init__(self):
        self.base_url = settings.STREAMTAPE_BASE_URL
        self.login = settings.STREAMTAPE_LOGIN
        self.key = settings.STREAMTAPE_KEY

    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal helper to make GET requests to the Streamtape API.
        """
        # Add common authentication parameters
        params_with_auth = {
            "login": self.login,
            "key": self.key,
            **params # Merge provided params
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params_with_auth)
                response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
                data = response.json()

                if data.get("status") == 200:
                    return data["result"]
                else:
                    raise HTTPException(
                        status_code=data.get("status", 500),
                        detail=data.get("msg", "An error occurred with the Streamtape API.")
                    )
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=500,
                    detail=f"An error occurred while requesting Streamtape API: {exc}"
                )
            except httpx.HTTPStatusError as exc:
                raise HTTPException(
                    status_code=exc.response.status_code,
                    detail=f"Error response from Streamtape API: {exc.response.status_code} - {exc.response.text}"
                )
            except Exception as exc:
                raise HTTPException(
                    status_code=500,
                    detail=f"An unexpected error occurred: {exc}"
                )

    async def get_upload_url(self, folder: Optional[str] = None, sha256: Optional[str] = None, httponly: Optional[bool] = None) -> Dict[str, Any]:
        """
        Retrieves a unique upload URL from Streamtape.
        """
        endpoint = "/file/ul"
        params: Dict[str, Any] = {}

        if folder:
            params["folder"] = folder
        if sha256:
            params["sha256"] = sha256
        if httponly is not None:
            params["httponly"] = str(httponly).lower()

        return await self._make_request(endpoint, params)

# Initialize the service to be used across endpoints
streamtape_service = StreamtapeService()