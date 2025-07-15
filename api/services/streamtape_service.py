import httpx
from fastapi import HTTPException
from config import settings
from typing import Dict, Any, Optional, Union

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
                    error_msg = data.get("msg", "An error occurred with the Streamtape API.")
                    # Streamtape sometimes returns specific error messages that are useful
                    if "result" in data and isinstance(data["result"], str):
                        error_msg = f"{error_msg}: {data['result']}"
                    raise HTTPException(
                        status_code=data.get("status", 500),
                        detail=error_msg
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

    async def add_remote_upload(
        self,
        url: str,
        folder: Optional[str] = None,
        headers: Optional[str] = None,
        name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Adds a remote upload task to Streamtape.
        """
        endpoint = "/remotedl/add"
        params: Dict[str, Any] = {"url": url}

        if folder:
            params["folder"] = folder
        if headers:
            params["headers"] = headers
        if name:
            params["name"] = name

        return await self._make_request(endpoint, params)

    async def remove_remote_upload(self, remote_upload_id: str) -> bool:
        """
        Removes/cancels a remote upload task on Streamtape.
        Set remote_upload_id to "all" to remove all remote uploads.
        """
        endpoint = "/remotedl/remove"
        params: Dict[str, Any] = {"id": remote_upload_id}

        result = await self._make_request(endpoint, params)
        # The API returns {"result": true} on success
        return result is True

    async def check_remote_upload_status(self, remote_upload_id: str) -> Dict[str, Any]:
        """
        Checks the status of a remote upload task on Streamtape.
        """
        endpoint = "/remotedl/status"
        params: Dict[str, Any] = {"id": remote_upload_id}

        return await self._make_request(endpoint, params)

# Initialize the service to be used across endpoints
streamtape_service = StreamtapeService()