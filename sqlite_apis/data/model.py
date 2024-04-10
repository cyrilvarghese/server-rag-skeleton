
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
 
 
class Tag(BaseModel):
    id:Optional[int] = None
    name: str
    description: str
    color: Optional[str] = None  # Optional field
    role_ids: List[int] = [] 
    class Config:
    # This will exclude default values (e.g., None or empty lists) from the output
        exclude_unset = True

class Job(BaseModel):
    id: int
    name: str

 
class Project(BaseModel):
    id:Optional[int] = None
    name: str
    description: str
    jobs: Optional[List[Job]] = []
    
# Pydantic model for project creation
class ProjectCreate(BaseModel):
    name: str
    description: str

 
 # Pydantic models for serialization
class File(BaseModel):
    id: int
    name: str
    created_at: str

class JobDetails(BaseModel):
    id: int
    name: str
    project_id: int
    tags: List[Tag]
    files: List[File]