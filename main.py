from fastapi import FastAPI
from api.endpoints import upload # Import the upload router

app = FastAPI(
    title="AuraHub API",
    description="A FastAPI application to wrap AuraHub API functionalities.",
    version="1.0.0"
)

# Include the routers for different functionalities
app.include_router(upload.router) # Now all upload endpoints are available under /streamtape

@app.get("/")
async def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "AuraHub API is running! Visit /docs for API endpoints."}

# The old /streamtape/get_download_link endpoint has been removed.