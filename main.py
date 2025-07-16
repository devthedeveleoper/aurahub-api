from fastapi import FastAPI
from api.endpoints import upload
from api.endpoints import file_management
from api.endpoints import converts
from api.endpoints import stream

app = FastAPI(
    title="AuraHub API",
    description="A FastAPI application to wrap AuraHub API functionalities.",
    version="1.0.0"
)

# Include the routers for different functionalities
app.include_router(upload.router)
app.include_router(file_management.router)
app.include_router(converts.router)
app.include_router(stream.router)

@app.get("/")
async def root():
    """
    Root endpoint to confirm the API is running.
    """
    return {"message": "AuraHub API Wrapper is running! Visit /docs for API endpoints."}