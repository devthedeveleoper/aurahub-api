import httpx
from fastapi import HTTPException
from config import settings
from typing import Dict, Any, Optional, Union, List

class StreamtapeService:
    """
    Service class to interact with the Streamtape API.
    Handles HTTP requests and common error responses.
    """
    def __init__(self):
        self.base_url = settings.STREAMTAPE_BASE_URL
        self.login = settings.STREAMTAPE_LOGIN
        self.key = settings.STREAMTAPE_KEY

    async def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Union[Dict[str, Any], List[Dict[str, Any]], str, bool]:
        """
        Internal helper to make GET requests to the Streamtape API.
        This method is now more flexible with its return type
        to accommodate different Streamtape API responses (dict, list, str, bool).
        """
        params_with_auth = {
            "login": self.login,
            "key": self.key,
            **params
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params_with_auth)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == 200:
                    return data["result"]
                else:
                    error_msg = data.get("msg", "An error occurred with the Streamtape API.")
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

    # --- Upload Related Methods ---
    async def get_upload_url(self, folder: Optional[str] = None, sha256: Optional[str] = None, httponly: Optional[bool] = None) -> Dict[str, Any]:
        endpoint = "/file/ul"
        params: Dict[str, Any] = {}
        if folder: params["folder"] = folder
        if sha256: params["sha256"] = sha256
        if httponly is not None: params["httponly"] = str(httponly).lower()
        return await self._make_request(endpoint, params) # type: ignore [return-value]

    async def add_remote_upload(
        self, url: str, folder: Optional[str] = None, headers: Optional[str] = None, name: Optional[str] = None
    ) -> Dict[str, Any]:
        endpoint = "/remotedl/add"
        params: Dict[str, Any] = {"url": url}
        if folder: params["folder"] = folder
        if headers: params["headers"] = headers
        if name: params["name"] = name
        return await self._make_request(endpoint, params) # type: ignore [return-value]

    async def remove_remote_upload(self, remote_upload_id: str) -> bool:
        endpoint = "/remotedl/remove"
        params: Dict[str, Any] = {"id": remote_upload_id}
        result = await self._make_request(endpoint, params)
        return result is True if isinstance(result, bool) else False

    async def check_remote_upload_status(self, remote_upload_id: str) -> Dict[str, Any]:
        endpoint = "/remotedl/status"
        params: Dict[str, Any] = {"id": remote_upload_id}
        result = await self._make_request(endpoint, params)
        return result if isinstance(result, dict) else {}

    # --- File/Folder Management Methods ---

    async def list_folder_contents(self, folder_id: str) -> Dict[str, Any]:
        endpoint = "/file/listfolder"
        params: Dict[str, Any] = {"folder": folder_id}
        result = await self._make_request(endpoint, params)
        return result if isinstance(result, dict) else {}

    async def create_folder(self, name: str, parent_folder_id: Optional[str] = None) -> Dict[str, str]:
        endpoint = "/file/createfolder"
        params: Dict[str, Any] = {"name": name}
        if parent_folder_id: params["pid"] = parent_folder_id
        result = await self._make_request(endpoint, params)
        return result if isinstance(result, dict) else {}

    async def rename_folder(self, folder_id: str, new_name: str) -> bool:
        endpoint = "/file/renamefolder"
        params: Dict[str, Any] = {"folder": folder_id, "name": new_name}
        result = await self._make_request(endpoint, params)
        return result is True if isinstance(result, bool) else False

    async def delete_folder(self, folder_id: str) -> bool:
        endpoint = "/file/deletefolder"
        params: Dict[str, Any] = {"folder": folder_id}
        result = await self._make_request(endpoint, params)
        return result is True if isinstance(result, bool) else False

    async def rename_file(self, file_id: str, new_name: str) -> bool:
        endpoint = "/file/rename"
        params: Dict[str, Any] = {"file": file_id, "name": new_name}
        result = await self._make_request(endpoint, params)
        return result is True if isinstance(result, bool) else False

    async def move_file(self, file_id: str, destination_folder_id: str) -> bool:
        endpoint = "/file/move"
        params: Dict[str, Any] = {"file": file_id, "folder": destination_folder_id}
        result = await self._make_request(endpoint, params)
        return result is True if isinstance(result, bool) else False

    async def delete_file(self, file_id: str) -> bool:
        endpoint = "/file/delete"
        params: Dict[str, Any] = {"file": file_id}
        result = await self._make_request(endpoint, params)
        return result is True if isinstance(result, bool) else False

    # --- Converts/Thumbnail Methods ---

    async def list_running_converts(self) -> List[Dict[str, Any]]:
        endpoint = "/file/runningconverts"
        params: Dict[str, Any] = {}
        result = await self._make_request(endpoint, params)
        if isinstance(result, list):
            return result
        raise HTTPException(status_code=500, detail="Unexpected response format for running converts list.")

    async def list_failed_converts(self) -> List[Dict[str, Any]]:
        endpoint = "/file/failedconverts"
        params: Dict[str, Any] = {}
        result = await self._make_request(endpoint, params)
        if isinstance(result, list):
            return result
        raise HTTPException(status_code=500, detail="Unexpected response format for failed converts list.")

    async def get_thumbnail_image(self, file_id: str) -> str:
        endpoint = "/file/getsplash"
        params: Dict[str, Any] = {"file": file_id}
        result = await self._make_request(endpoint, params)
        if isinstance(result, str):
            return result
        raise HTTPException(status_code=500, detail="Unexpected response format for thumbnail URL.")

    # --- Stream Related Methods (New) ---

    async def get_download_ticket(self, file_id: str) -> Dict[str, Any]:
        """
        Prepares a download ticket for a given file.
        """
        endpoint = "/file/dlticket"
        # Login and Key are automatically added by _make_request if they are in params_with_auth
        params: Dict[str, Any] = {"file": file_id}
        result = await self._make_request(endpoint, params)
        if isinstance(result, dict):
            return result
        raise HTTPException(status_code=500, detail="Unexpected response format for download ticket.")

    async def get_final_download_link(self, file_id: str, ticket: str, captcha_response: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieves the final download link using a download ticket.
        Note: This specific API endpoint from Streamtape does NOT require login/key.
        """
        endpoint = "/file/dl"
        params: Dict[str, Any] = {
            "file": file_id,
            "ticket": ticket,
        }
        if captcha_response:
            params["captcha_response"] = captcha_response
        
        # For this specific endpoint, we will NOT use _make_request as it adds login/key
        # and the Streamtape docs state it's not needed, and we want to ensure it's not sent.
        # So we'll make a direct httpx call here.
        async with httpx.AsyncClient() as client:
            try:
                # IMPORTANT: No login/key added here, as per your requirement and Streamtape docs
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == 200:
                    return data["result"]
                else:
                    error_msg = data.get("msg", "An error occurred with the Streamtape API.")
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

    async def get_file_info(self, file_ids: Union[str, List[str]]) -> Dict[str, Any]:
        """
        Checks the status and details of one or more files.
        """
        endpoint = "/file/info"
        
        # Convert list of file IDs to comma-separated string if necessary
        file_id_string = file_ids if isinstance(file_ids, str) else ",".join(file_ids)

        params: Dict[str, Any] = {"file": file_id_string}
        result = await self._make_request(endpoint, params)
        if isinstance(result, dict):
            return result
        raise HTTPException(status_code=500, detail="Unexpected response format for file info.")


# Initialize the service to be used across endpoints
streamtape_service = StreamtapeService()