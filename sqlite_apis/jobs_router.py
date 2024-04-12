import shutil
from fastapi import APIRouter
from typing import List
import sqlite3

from fastapi import UploadFile, File, Form
import sqlite3
from datetime import datetime
import os
 
from sqlite_apis.data.db_sql import get_db_connection

jobs_router = APIRouter();

 

# Ensure the upload directory exists
upload_dir = "../server/uploads"
os.makedirs(upload_dir, exist_ok=True)
conn=get_db_connection()

def create_job(project_id: int, name: str, description: str, conn):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Jobs (project_id, name, created_at)
        VALUES (?, ?, ?)
    """, (project_id, name, datetime.now()))
    job_id = cursor.lastrowid
    conn.commit()
    return job_id

def save_file(file: UploadFile, job_id: int, project_id: int, conn):
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Files (name, job_id, project_id, created_at)
        VALUES (?, ?, ?, ?)
    """, (file.filename, job_id, project_id, datetime.now()))
    conn.commit()

@jobs_router.post("/")
async def create_job_with_files(
    project_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    files: List[UploadFile] = File(...) 
):
     
    job_id = create_job(project_id, name, description, conn)
    
    for file in files:
        save_file(file, job_id, project_id, conn)

    return {"message": "Job and files created successfully", "job_id": job_id}

