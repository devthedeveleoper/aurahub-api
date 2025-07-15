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

    # --- Upload Related Methods (Existing) ---
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
        return result is True # API returns {"result": true} on success

    async def check_remote_upload_status(self, remote_upload_id: str) -> Dict[str, Any]:
        """
        Checks the status of a remote upload task on Streamtape.
        """
        endpoint = "/remotedl/status"
        params: Dict[str, Any] = {"id": remote_upload_id}

        return await self._make_request(endpoint, params)

    # --- File/Folder Management Methods (New) ---

    async def list_folder_contents(self, folder_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Shows the content (folders and files) of a given Streamtape folder.
        If folder_id is not provided, lists root folder contents.
        """
        endpoint = "/file/listfolder"
        params: Dict[str, Any] = {}
        if folder_id:
            params["folder"] = folder_id
        return await self._make_request(endpoint, params)

    async def create_folder(self, name: str, parent_folder_id: Optional[str] = None) -> Dict[str, str]:
        """
        Creates a new folder on Streamtape.
        """
        endpoint = "/file/createfolder"
        params: Dict[str, Any] = {"name": name}
        if parent_folder_id:
            params["pid"] = parent_folder_id
        return await self._make_request(endpoint, params)

    async def rename_folder(self, folder_id: str, new_name: str) -> bool:
        """
        Renames a folder on Streamtape.
        """
        endpoint = "/file/renamefolder"
        params: Dict[str, Any] = {"folder": folder_id, "name": new_name}
        result = await self._make_request(endpoint, params)
        return result is True

    async def delete_folder(self, folder_id: str) -> bool:
        """
        Deletes a folder and all its contents (subfolders and files) on Streamtape.
        """
        endpoint = "/file/deletefolder"
        params: Dict[str, Any] = {"folder": folder_id}
        result = await self._make_request(endpoint, params)
        return result is True

    async def rename_file(self, file_id: str, new_name: str) -> bool:
        """
        Renames a file on Streamtape.
        """
        endpoint = "/file/rename"
        params: Dict[str, Any] = {"file": file_id, "name": new_name}
        result = await self._make_request(endpoint, params)
        return result is True

    async def move_file(self, file_id: str, destination_folder_id: str) -> bool:
        """
        Moves a file into a different folder on Streamtape.
        """
        endpoint = "/file/move"
        params: Dict[str, Any] = {"file": file_id, "folder": destination_folder_id}
        result = await self._make_request(endpoint, params)
        return result is True

    async def delete_file(self, file_id: str) -> bool:
        """
        Deletes a file from Streamtape.
        """
        endpoint = "/file/delete"
        params: Dict[str, Any] = {"file": file_id}
        result = await self._make_request(endpoint, params)
        return result is True


# Initialize the service to be used across endpoints
streamtape_service = StreamtapeService()