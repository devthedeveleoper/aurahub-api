from fastapi import APIRouter, HTTPException, Query, Body # Keep Body for now, in case you need it elsewhere
from typing import Optional, Dict, Any, Union
from api.services.streamtape_service import streamtape_service

# Create an APIRouter instance
router = APIRouter(
    prefix="/streamtape", # All endpoints in this router will start with /streamtape
    tags=["Upload"] # Group these endpoints under the "Upload" tag in Swagger UI
)

@router.get("/get_upload_url", response_model=Dict[str, Any])
async def get_upload_url_endpoint(
    folder: Optional[str] = Query(None, description="Optional Folder-ID to upload to"),
    sha256: Optional[str] = Query(None, description="Optional expected SHA256 of the file for validation"),
    httponly: Optional[bool] = Query(None, description="If true, use only HTTP upload links (not recommended for production)")
):
    """
    Retrieves a unique upload URL from AuraHub. Files shall be POSTed to this URL.

    Args:
        folder (str, optional): The ID of the folder to upload the file to.
        sha256 (str, optional): The expected SHA256 hash of the file. If the uploaded file's hash
                                doesn't match, the upload will fail.
        httponly (bool, optional): If set to true, AuraHub will return HTTP upload links.
                                   It's recommended to use HTTPS, so this should generally be False or None.

    Returns:
        dict: A dictionary containing the upload URL and its validity period.
    """
    try:
        # Call the service layer to get the upload URL
        upload_info = await streamtape_service.get_upload_url(
            folder=folder,
            sha256=sha256,
            httponly=httponly
        )
        return upload_info
    except HTTPException as e:
        raise e # Re-raise FastAPI HTTPExceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

# --- Remote Upload Endpoints ---

@router.post("/remote_upload/add", response_model=Dict[str, str])
async def add_remote_upload_endpoint(
    # CHANGED: Use Query(...) for parameters instead of Body(...)
    url: str = Query(..., description="The remote URL of the file to upload"),
    folder: Optional[str] = Query(None, description="Optional Folder-ID to upload to"),
    headers: Optional[str] = Query(None, description="Additional HTTP headers (e.g. 'Cookie: key=value'), separated by newlines"),
    name: Optional[str] = Query(None, description="Custom name for the new file (optional)")
):
    """
    Adds a remote upload task to AuraHub.

    Args:
        url (str): The direct URL of the remote file to be uploaded.
        folder (str, optional): The ID of the folder to upload the file to.
        headers (str, optional): Additional HTTP headers for the remote server (e.g., for authentication).
        name (str, optional): A custom name for the uploaded file.

    Returns:
        dict: A dictionary containing the ID of the remote upload task and the folder ID.
    """
    try:
        remote_upload_info = await streamtape_service.add_remote_upload(
            url=url,
            folder=folder,
            headers=headers,
            name=name
        )
        return remote_upload_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.delete("/remote_upload/remove/{remote_upload_id}", response_model=Dict[str, bool])
async def remove_remote_upload_endpoint(
    remote_upload_id: str
):
    """
    Removes or cancels a remote upload task on AuraHub.

    Args:
        remote_upload_id (str): The ID of the remote upload to remove, or "all" to remove all remote uploads.

    Returns:
        dict: A dictionary indicating success ({"result": true}).
    """
    try:
        success = await streamtape_service.remove_remote_upload(remote_upload_id=remote_upload_id)
        return {"result": success}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/remote_upload/status/{remote_upload_id}", response_model=Dict[str, Any])
async def check_remote_upload_status_endpoint(
    remote_upload_id: str
):
    """
    Checks the status of a specific remote upload task on AuraHub.

    Args:
        remote_upload_id (str): The ID of the remote upload to check.

    Returns:
        dict: A dictionary containing the status details of the remote upload.
    """
    try:
        status_info = await streamtape_service.check_remote_upload_status(remote_upload_id=remote_upload_id)
        return status_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")