from fastapi import APIRouter,HTTPException
from typing import List, Optional
from pydantic import BaseModel
import sqlite3

from sqlite_apis.data.model import File, JobDetails, Tag

jobs_router = APIRouter();


db_path = '../server/sqlite_apis/data/singular-db.sqlite'
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@jobs_router.get("/{job_id}", response_model=JobDetails)
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
    cursor.execute("SELECT id, name FROM Files WHERE job_id = ?", (job_id,))
    files = cursor.fetchall()

    # Close the connection
    conn.close()

    # Step 5 & 7: Combine the data and return it
    return JobDetails(
        id=job['id'],
        name=job['name'],
        project_id=job['project_id'],
        tags=[Tag(id=tag['id'], name=tag['name'], description=tag['description'], color=tag['color']) for tag in tags],
        files=[File(id=file['id'], name=file['name']) for file in files]
    )