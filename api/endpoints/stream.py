from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, Dict, Any, List, Union
from api.services.streamtape_service import streamtape_service

# Create an APIRouter instance for streaming functionalities
router = APIRouter(
    prefix="/streamtape", # All endpoints in this router will start with /streamtape
    tags=["Stream & Info"] # Group these endpoints under a new tag
)

@router.get("/stream/ticket/{file_id}", response_model=Dict[str, Any])
async def get_download_ticket_endpoint(
    file_id: str = Path(..., description="The ID of the file for which to get a download ticket.")
):
    """
    Prepares a download ticket for a given Streamtape file. This ticket is required
    to obtain the final download link and ensures privacy by not exposing API credentials.

    Args:
        file_id (str): The unique ID of the file.

    Returns:
        dict: A dictionary containing the ticket, wait time, and valid_until information.
    """
    try:
        ticket_info = await streamtape_service.get_download_ticket(file_id=file_id)
        return ticket_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/stream/link/{file_id}", response_model=Dict[str, Any])
async def get_final_download_link_endpoint(
    file_id: str = Path(..., description="The ID of the file."),
    ticket: str = Query(..., description="The previously generated download ticket."),
    captcha_response: Optional[str] = Query(None, description="Optional captcha response if required by Streamtape.")
):
    """
    Retrieves the final direct download link for a file using a valid download ticket.
    Your API credentials are NOT used for this external Streamtape API call.

    Args:
        file_id (str): The unique ID of the file.
        ticket (str): The download ticket obtained from the /stream/ticket endpoint.
        captcha_response (str, optional): A response from a captcha if Streamtape requires it.

    Returns:
        dict: A dictionary containing the file name, size, and the direct download URL.
    """
    try:
        download_link_info = await streamtape_service.get_final_download_link(
            file_id=file_id,
            ticket=ticket,
            captcha_response=captcha_response
        )
        return download_link_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.get("/file_info/{file_ids}", response_model=Dict[str, Any])
async def get_file_info_endpoint(
    file_ids: str = Path(..., description="Comma-separated File-IDs (e.g., 'id1,id2,id3') for which to get information. Max 100.")
):
    """
    Checks the status and detailed information of one or more files on Streamtape.
    Your API credentials are NOT exposed in this endpoint.

    Args:
        file_ids (str): A single file ID or a comma-separated string of multiple file IDs (max 100).

    Returns:
        dict: A dictionary where keys are file IDs and values are their respective information (name, size, status, etc.).
    """
    try:
        # The service method can handle both single string and list of strings
        # We pass the comma-separated string directly.
        info = await streamtape_service.get_file_info(file_ids=file_ids)
        return info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")