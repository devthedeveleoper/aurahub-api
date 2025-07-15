from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Dict, Any
from api.services.streamtape_service import streamtape_service

# Create an APIRouter instance for converts and thumbnail management
router = APIRouter(
    prefix="/streamtape", # All endpoints in this router will start with /streamtape
    tags=["Converts & Thumbnails"] # Group these endpoints under a new tag
)

@router.get("/converts/running", response_model=List[Dict[str, Any]])
async def list_running_converts_endpoint():
    """
    Lists all video conversion tasks that are currently running on Streamtape, including their progress.

    Returns:
        list: A list of dictionaries, each representing a running conversion.
    """
    try:
        converts_list = await streamtape_service.list_running_converts()
        return converts_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/converts/failed", response_model=List[Dict[str, Any]])
async def list_failed_converts_endpoint():
    """
    Lists all video conversion tasks that have failed on Streamtape.

    Returns:
        list: A list of dictionaries, each representing a failed conversion.
    """
    try:
        converts_list = await streamtape_service.list_failed_converts()
        return converts_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/thumbnail/{file_id}", response_model=Dict[str, str])
async def get_thumbnail_image_endpoint(
    file_id: str = Path(..., description="The ID of the file for which to retrieve the thumbnail.")
):
    """
    Retrieves the direct URL to the thumbnail image of a specific video file.

    Args:
        file_id (str): The unique ID of the video file.

    Returns:
        dict: A dictionary containing the URL to the thumbnail image (e.g., {"thumbnail_url": "https://..."}).
    """
    try:
        thumbnail_url = await streamtape_service.get_thumbnail_image(file_id=file_id)
        return {"thumbnail_url": thumbnail_url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")