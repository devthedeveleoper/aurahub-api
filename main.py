from fastapi import FastAPI
from api.endpoints import upload
from api.endpoints import file_management
from api.endpoints import converts # Import the new converts router

app = FastAPI(
    title="Streamtape API Wrapper",
    description="A FastAPI application to wrap Streamtape API functionalities.",
    version="1.0.0"
)

# Include the routers for different functionalities
app.include_router(upload.router)
app.include_router(file_management.router)
app.include_router(converts.router) # Include the new router here

@app.get("/")
async def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "Streamtape API Wrapper is running! Visit /docs for API endpoints."}