from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional, Dict, Any, Union
from api.services.streamtape_service import streamtape_service

# Create an APIRouter instance for file/folder management
router = APIRouter(
    prefix="/streamtape", # All endpoints in this router will start with /streamtape
    tags=["File/Folder Management"] # Group these endpoints under a new tag
)

@router.get("/file_manager/list_contents", response_model=Dict[str, Any])
async def list_folder_contents_endpoint(
    folder_id: Optional[str] = Query(None, description="Optional Folder-ID to list contents from. If not provided, lists root.")
):
    """
    Shows the content (folders and files) of a given Streamtape folder.
    If no folder_id is provided, it lists the contents of the root folder.

    Args:
        folder_id (str, optional): The ID of the folder whose contents you want to list.

    Returns:
        dict: A dictionary containing lists of folders and files.
    """
    try:
        contents = await streamtape_service.list_folder_contents(folder_id=folder_id)
        return contents
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.post("/file_manager/create_folder", response_model=Dict[str, str])
async def create_folder_endpoint(
    name: str = Query(..., description="Name of the new folder to create."),
    parent_folder_id: Optional[str] = Query(None, description="Optional Parent Folder ID. If not set, folder will be created in the root.")
):
    """
    Creates a new folder on Streamtape.

    Args:
        name (str): The name of the new folder.
        parent_folder_id (str, optional): The ID of the parent folder where this new folder will be created.

    Returns:
        dict: A dictionary containing the ID of the newly created folder.
    """
    try:
        new_folder_info = await streamtape_service.create_folder(name=name, parent_folder_id=parent_folder_id)
        return new_folder_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.put("/file_manager/rename_folder/{folder_id}", response_model=Dict[str, bool])
async def rename_folder_endpoint(
    folder_id: str = Path(..., description="The ID of the folder to rename."),
    new_name: str = Query(..., description="The new name for the folder.")
):
    """
    Renames an existing folder on Streamtape.

    Args:
        folder_id (str): The ID of the folder to rename.
        new_name (str): The new name for the folder.

    Returns:
        dict: A dictionary indicating success ({"result": true}).
    """
    try:
        success = await streamtape_service.rename_folder(folder_id=folder_id, new_name=new_name)
        return {"result": success}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.delete("/file_manager/delete_folder/{folder_id}", response_model=Dict[str, bool])
async def delete_folder_endpoint(
    folder_id: str = Path(..., description="The ID of the folder to delete (all contents will be lost!).")
):
    """
    Deletes a folder and all its contents (subfolders and files) on Streamtape. Be careful!

    Args:
        folder_id (str): The ID of the folder to delete.

    Returns:
        dict: A dictionary indicating success ({"result": true}).
    """
    try:
        success = await streamtape_service.delete_folder(folder_id=folder_id)
        return {"result": success}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.put("/file_manager/rename_file/{file_id}", response_model=Dict[str, bool])
async def rename_file_endpoint(
    file_id: str = Path(..., description="The ID of the file to rename."),
    new_name: str = Query(..., description="The new name for the file (including extension, e.g., 'video.mp4').")
):
    """
    Renames a file on Streamtape.

    Args:
        file_id (str): The ID of the file to rename.
        new_name (str): The new name for the file.

    Returns:
        dict: A dictionary indicating success ({"result": true}).
    """
    try:
        success = await streamtape_service.rename_file(file_id=file_id, new_name=new_name)
        return {"result": success}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.put("/file_manager/move_file/{file_id}", response_model=Dict[str, bool])
async def move_file_endpoint(
    file_id: str = Path(..., description="The ID of the file to move."),
    destination_folder_id: str = Query(..., description="The ID of the destination folder.")
):
    """
    Moves a file into a different folder on Streamtape.

    Args:
        file_id (str): The ID of the file to move.
        destination_folder_id (str): The ID of the target folder where the file will be moved.

    Returns:
        dict: A dictionary indicating success ({"result": true}).
    """
    try:
        success = await streamtape_service.move_file(file_id=file_id, destination_folder_id=destination_folder_id)
        return {"result": success}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")

@router.delete("/file_manager/delete_file/{file_id}", response_model=Dict[str, bool])
async def delete_file_endpoint(
    file_id: str = Path(..., description="The ID of the file to delete.")
):
    """
    Deletes a file from Streamtape.

    Args:
        file_id (str): The ID of the file to delete.

    Returns:
        dict: A dictionary indicating success ({"result": true}).
    """
    try:
        success = await streamtape_service.delete_file(file_id=file_id)
        return {"result": success}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")