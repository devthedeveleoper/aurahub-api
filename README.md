# 🚀 Streamtape API Wrapper (FastAPI)

Welcome to the Streamtape API Wrapper! This project provides a robust and easy-to-use interface to interact with the Streamtape.com API, built with **FastAPI** for high performance and excellent developer experience. It abstracts away the complexities of direct API calls, offering well-defined endpoints for file uploads, remote uploads, file/folder management, conversion status checks, and direct file streaming.

## ✨ Features

* **Secure API Key Handling**: Your Streamtape API `login` and `key` are securely stored in environment variables and are never exposed in client-side requests.
* **Modular Design**: Organized into FastAPI routers and a dedicated service layer for clear separation of concerns.
* **Comprehensive Endpoints**: Covers a wide range of Streamtape functionalities:
    * **File Uploads**: Obtain upload URLs and manage remote uploads.
    * **File & Folder Management**: List contents, create, rename, move, and delete files/folders.
    * **Conversion Monitoring**: Check the status of running and failed video conversions.
    * **Thumbnail Retrieval**: Get direct links to video thumbnails.
    * **Secure Streaming**: Generate download tickets and obtain direct streaming links for files without exposing your API credentials.
* **Automatic Interactive Documentation**: Powered by Swagger UI (OpenAPI), making it easy to test and understand all API endpoints directly from your browser.
* **Asynchronous Operations**: Built with `asyncio` and `httpx` for efficient, non-blocking I/O operations, ensuring your API remains responsive.
* **Pylance Type Hinting**: Strong type hinting throughout the codebase for improved readability, maintainability, and error prevention.

## 🛠️ Technologies Used

* **Python 3.9+**
* **FastAPI**: For building the web API.
* **Uvicorn**: ASGI server for running the FastAPI application.
* **HTTPX**: A robust, asynchronous HTTP client for making requests to the Streamtape API.
* **Pydantic**: For data validation and settings management.

## 🚀 Getting Started

Follow these steps to set up and run your Streamtape API Wrapper.

### Prerequisites

* Python 3.9 or higher installed.
* A Streamtape.com account and your API `login` and `key`. You can find them on your [Streamtape API page](https://streamtape.com/account?api).

### 1. Clone the Repository

```bash
git clone <repository_url>
cd streamtape_wrapper # Navigate into your project directory
````

### 2\. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` yet, create one with the following content and then run the command:

```
# requirements.txt
fastapi
uvicorn[standard]
httpx
pydantic-settings # Or pydantic if you're using an older version
```

### 4\. Configure Environment Variables

Create a `.env` file in the root of your project directory (`streamtape_wrapper/`) and add your Streamtape API credentials:

```ini
# .env
STREAMTAPE_BASE_URL="[https://api.streamtape.com](https://api.streamtape.com)"
STREAMTAPE_LOGIN="your_streamtape_api_login"
STREAMTAPE_KEY="your_streamtape_api_key"
```

**Replace `"your_streamtape_api_login"` and `"your_streamtape_api_key"` with your actual credentials.**

### 5\. Run the Application

```bash
uvicorn main:app --reload
```

The `--reload` flag is great for development as it automatically restarts the server on code changes.

-----

## 🖥️ API Endpoints & Usage

Once the server is running, you can access the interactive API documentation (Swagger UI) in your browser:

👉 [http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)

Here's a breakdown of the available endpoint categories:

### Root Endpoint

  * **`GET /`**: Basic endpoint to confirm the API is running.

-----

### ⬆️ Upload Endpoints (`/streamtape`)

These endpoints facilitate file uploads and remote URL processing.

  * **`GET /streamtape/get_upload_url`**: Get a one-time URL for direct file uploads.
      * Parameters: `folder` (optional), `sha256` (optional), `httponly` (optional).
  * **`POST /streamtape/remote_upload/add`**: Initiate a remote upload from a given URL.
      * Parameters: `url` (required), `folder` (optional), `headers` (optional), `name` (optional).
  * **`DELETE /streamtape/remote_upload/remove/{remote_upload_id}`**: Cancel or remove a remote upload task.
      * Path Parameter: `remote_upload_id` (required, or "all").
  * **`GET /streamtape/remote_upload/status/{remote_upload_id}`**: Check the status of a specific remote upload.
      * Path Parameter: `remote_upload_id` (required).

-----

### 📂 File/Folder Management Endpoints (`/streamtape`)

Manage your files and folders directly.

  * **`POST /streamtape/file_manager/create_folder`**: Create a new folder.
      * Query Parameters: `name` (required), `parent_folder_id` (optional).
  * **`GET /streamtape/file_manager/list_contents`**: List contents (files and subfolders) of a specified folder.
      * Query Parameter: `folder_id` (required).
  * **`PUT /streamtape/file_manager/rename_folder/{folder_id}`**: Rename an existing folder.
      * Path Parameter: `folder_id` (required).
      * Query Parameter: `new_name` (required).
  * **`DELETE /streamtape/file_manager/delete_folder/{folder_id}`**: Delete a folder and all its contents. **Use with caution\!**
      * Path Parameter: `folder_id` (required).
  * **`PUT /streamtape/file_manager/rename_file/{file_id}`**: Rename an existing file.
      * Path Parameter: `file_id` (required).
      * Query Parameter: `new_name` (required).
  * **`PUT /streamtape/file_manager/move_file/{file_id}`**: Move a file to a different folder.
      * Path Parameter: `file_id` (required).
      * Query Parameter: `destination_folder_id` (required).
  * **`DELETE /streamtape/file_manager/delete_file/{file_id}`**: Delete a file.
      * Path Parameter: `file_id` (required).

-----

### 🔄 Converts & Thumbnails Endpoints (`/streamtape`)

Monitor conversion processes and retrieve thumbnails.

  * **`GET /streamtape/converts/running`**: Lists all currently running video conversion tasks.
  * **`GET /streamtape/converts/failed`**: Lists all video conversion tasks that have failed.
  * **`GET /streamtape/thumbnail/{file_id}`**: Get the URL for a video's thumbnail image.
      * Path Parameter: `file_id` (required).

-----

### 🔗 Stream & Info Endpoints (`/streamtape`)

Securely obtain download links and file metadata without exposing API keys.

  * **`GET /streamtape/stream/ticket/{file_id}`**: Get a download ticket for a file. This ticket is short-lived and required for the final download link. Your API credentials are used *internally* by the wrapper for this step, but not exposed externally.
      * Path Parameter: `file_id` (required).
  * **`GET /streamtape/stream/link/{file_id}`**: Get the final direct download URL using a valid ticket. **Your API credentials are NOT used for this external Streamtape API call.**
      * Path Parameter: `file_id` (required).
      * Query Parameters: `ticket` (required), `captcha_response` (optional).
  * **`GET /streamtape/file_info/{file_ids}`**: Get detailed information (status, size, etc.) for one or more files. **Your API credentials are NOT exposed externally in this endpoint.**
      * Path Parameter: `file_ids` (required, comma-separated string of IDs).

-----

## 🤝 Contributing

Contributions are welcome\! If you find a bug or want to add a new feature, please open an issue or submit a pull request.

## 📄 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).
