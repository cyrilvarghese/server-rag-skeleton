from fastapi import FastAPI
import chroma_setup
from modules.routers.files_router import files_router
from modules.routers.upload_router import upload_router 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# Add middleware to the app

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins (you can restrict this to specific origins)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allow these HTTP methods
    allow_headers=["*"],  # Allow all headers
)
app.mount("/files", StaticFiles(directory="uploads"), name="static")
# Define a startup event handler to call setup_chroma asynchronously
@app.on_event("startup")
async def startup_event():
    await chroma_setup.setup_chroma(is_reset=True)

# Include routers for different endpoints
app.include_router(upload_router, prefix="/api/upload")
app.include_router(files_router, prefix="/api/files")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}