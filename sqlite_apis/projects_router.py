from fastapi import APIRouter, HTTPException,status,Depends
import asyncio
import sqlite3
 
from typing import Any, Dict, List, Optional, Annotated
from pydantic import BaseModel, Field
from sqlite_apis.data.model import UploadedFile, Job, JobDetails, Project, ProjectCreate, Tag
 
projects_router = APIRouter();

db_path = '../server/sqlite_apis/data/singular-db.sqlite'
 



def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@projects_router.get("/", response_model=List[Project])
async def read_projects():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Fetch projects
    cursor.execute("SELECT * FROM Projects")
    projects_rows = cursor.fetchall()
    
    projects = []
    for project_row in projects_rows:
        # For each project, fetch associated jobs (IDs and names)
        cursor.execute("SELECT id, name,created_at FROM Jobs WHERE project_id = ?", (project_row['id'],))
        jobs = cursor.fetchall()
        
        projects.append(Project(
            id=project_row['id'],
            name=project_row['name'],
            description=project_row['description'],
            jobs=[Job(id=job['id'], name=job['name'],created_at=job["created_at"]) for job in jobs]
        ))
    
    conn.close()
    

    return projects

@projects_router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Projects (name, description) VALUES (?, ?)",
                   (project.name, project.description))
    new_project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return {**project.model_dump(), "id": new_project_id}



@projects_router.get("/{project_id}", response_model=Project)
async def read_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch the specific project
    cursor.execute("SELECT * FROM Projects WHERE id = ?", (project_id,))
    project_row = cursor.fetchone()
    
    if project_row is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Fetch associated jobs for the specific project
    cursor.execute("SELECT id, name,created_at FROM Jobs WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
    jobs = cursor.fetchall()
    
    project = Project(
        id=project_row['id'],
        name=project_row['name'],
        description=project_row['description'],
        jobs=[Job(id=job['id'], name=job['name'],created_at=job['created_at']) for job in jobs]
    )
    
    conn.close()
    return project

@projects_router.put("/{project_id}", response_model=Project)
async def update_project(project_id: int, project: ProjectCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Projects SET name = ?, description = ? WHERE id = ?",
                   (project.name, project.description, project_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    conn.commit()
    conn.close()
    return {**project.model_dump(), "id": project_id}

@projects_router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Projects WHERE id = ?", (project_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    conn.commit()
    conn.close()
    return {"message": "Project deleted successfully"}

 
@projects_router.get("/{project_id}/jobs/{job_id}", response_model=JobDetails)
def get_job_by_id(job_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Step 2: Fetch the job
    cursor.execute("SELECT * FROM Jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Step 3: Fetch project tags
   # Adjusted SQL Query for Fetching Tags (assuming `description` and `color` are available in the `Tags` table)
    cursor.execute("""
        SELECT t.id, t.name, t.description, t.color 
        FROM Tags t 
        JOIN Projects_Tags pt ON t.id = pt.tag_id 
        WHERE pt.project_id = ?
    """, (job['project_id'],))
    tags = cursor.fetchall()  

    # Step 4: Fetch job files
    cursor.execute("SELECT id, name ,created_at FROM Files WHERE job_id = ?", (job_id,))
    files = cursor.fetchall()

    # Close the connection
    conn.close()

    # Step 5 & 7: Combine the data and return it
    return JobDetails(
        id=job['id'],
        name=job['name'],
        project_id=job['project_id'],
        tags=[Tag(id=tag['id'], name=tag['name'], description=tag['description'], color=tag['color']) for tag in tags],
        files=[UploadedFile(id=file['id'], name=file['name'],created_at=file['created_at']) for file in files]
    )

@projects_router.get("/{project_id}/files", response_model=List[UploadedFile])
def get_files_by_project(project_id: int):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, created_at FROM Files WHERE project_id = ?
    """, (project_id,))
    
    files_rows = cursor.fetchall()
    if not files_rows:
        raise HTTPException(status_code=404, detail="No files found for the given project ID")
    
    files = [UploadedFile(id=row['id'], name=row['name'], created_at=row['created_at']) for row in files_rows]
    
    conn.close()
    return files

@projects_router.get("/{project_id}/tags", response_model=List[Tag])
async def read_tags_by_project(project_id: int):
    """API endpoint to fetch tags associated with a project ID."""
    try:
        tags = get_tags_by_project_id(project_id)
        if not tags:
            raise HTTPException(status_code=404, detail="No tags found for this project")
        return tags
    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    


def get_tags_by_project_id(project_id: int) -> List[Dict[str, Any]]:
    """Retrieve tags for a given project ID from the database."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Tags.id, Tags.name, Tags.description, Tags.color
        FROM Tags
        INNER JOIN Projects_Tags ON Tags.id = Projects_Tags.tag_id
        WHERE Projects_Tags.project_id = ?
    """, (project_id,))

    rows = cursor.fetchall()
    tags = [dict(row) for row in rows]

    cursor.close()
    conn.close()

    return tags