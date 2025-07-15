from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
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
    Retrieves a unique upload URL from Streamtape. Files shall be POSTed to this URL.

    Args:
        folder (str, optional): The ID of the folder to upload the file to.
        sha256 (str, optional): The expected SHA256 hash of the file. If the uploaded file's hash
                                doesn't match, the upload will fail.
        httponly (bool, optional): If set to true, Streamtape will return HTTP upload links.
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

# You can add more upload-related endpoints here, e.g., for direct file upload via your API.
# We'll cover that in a later step!