from fastapi import FastAPI
import chroma_setup
from modules.routers.files_router import files_router
from modules.routers.upload_router import upload_router 
from modules.routers.query_router import query_router 
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from config import BASE_PATH
from modules.routers.qq_LLM_router import qq_LLM_router
from sqlite_apis.tags_router import tags_router
from sqlite_apis.projects_router import projects_router
from sqlite_apis.jobs_router import jobs_router
from sqlite_apis.roles_router import roles_router
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
app.mount("/uploads", StaticFiles(directory="../server/uploads"), name="static")
# Define a startup event handler to call setup_chroma asynchronously
@app.on_event("startup")
async def startup_event():
    await chroma_setup.setup_chroma(is_reset=False)

# Include routers for different endpoints
app.include_router(query_router, prefix="/api/query")
app.include_router(upload_router, prefix="/api/upload")
app.include_router(files_router, prefix="/api/files")
app.include_router(tags_router, prefix="/api/tags")
app.include_router(qq_LLM_router, prefix="/api/data")
app.include_router(projects_router, prefix="/api/projects")
app.include_router(jobs_router, prefix="/api/jobs")
app.include_router(roles_router, prefix="/api/roles")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}