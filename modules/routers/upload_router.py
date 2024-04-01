 # upload_router.py

import os 
from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List
import json
from modules.file_processor import process_files

upload_router = APIRouter()
 

@upload_router.post("/")
async def upload_pdfs(pdf_files: list[UploadFile] = File(...)):
    response = {"message": "PDF files uploaded successfully.", "uploaded_files": []}
 
    for pdf_file in pdf_files:
        
        if not pdf_file.filename.endswith('.pdf'):
            return {"error": "Only PDF files are allowed."}
        # Specify the directory where files will be saved
        upload_folder = "../server/uploads"
        os.makedirs(upload_folder, exist_ok=True)  # Create the directory if it doesn't exist
        
        # Save the PDF file to the specified directory
        file_path = os.path.join(upload_folder, pdf_file.filename)
        # Process the PDF file (for example, save it to disk)
        with open(file_path, "wb") as file_object:
            file_object.write(await pdf_file.read())
            

        response["uploaded_files"].append(pdf_file.filename)
        
    await process_files();    
    return response

@upload_router.get("/")
async def get_upload():
    return {"message": "GET Upload route"}
 