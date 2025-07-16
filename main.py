from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from api.endpoints import upload
from api.endpoints import file_management
from api.endpoints import converts
from api.endpoints import stream
from config import settings # Import your settings

app = FastAPI(
    title="AuraHub API",
    description="A FastAPI application to wrap AuraHub API functionalities.",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, # Use the origins loaded from settings
    allow_credentials=True,                # Allow cookies/authorization headers to be sent
    allow_methods=["*"],                   # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],                   # Allow all headers in the request
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