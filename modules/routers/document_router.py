# query_router.py
from typing import List
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from modules.db import get_LC_chroma_client 
from modules.get_retriever import get_retriever  # Adjust the path accordingly
from modules.cross_encoder_rerank import get_reranked_docs

load_dotenv()
document_router = APIRouter()
 

@document_router.post('/')
async def get_chunks(req_body: dict):
    file_names = req_body.get("fileNames")
    if not file_names:
        raise HTTPException(status_code=400, detail="No file names provided.")

    results = []
    for file_name in file_names:
        try:
            result = filter_collection_by_metadata(file_name)
            results.append(result)
        except Exception as e:
            # Log the error and return a message specific to the error encountered
            print(f"Error processing file {file_name}: {str(e)}")
            results.append({"file": file_name, "error": "Failed to process due to an internal error"})

    return {"results": results}

def filter_collection_by_metadata(file_name: str):
    # Placeholder function - replace with your actual logic
    # Assuming some operation that could raise an error
    print(f"Filtering collection for file: {file_name}")
    file_path= "../server/uploads/"+file_name;
    filtered_collection = get_LC_chroma_client().get(where={"source": file_path})
    results = combine_data(filtered_collection["ids"],filtered_collection["metadatas"],filtered_collection["documents"])
    # Simulate filtering logic
    return results


def combine_data(ids, metadatas, documents):
    combined_results = []
    # Ensure all arrays have the same length
    if not (len(ids) == len(metadatas) == len(documents)):
        raise ValueError("The length of ids, metadatas, and documents must be the same.")
    
    # Combine data
    for i in range(len(ids)):
        combined_results.append({
            "id": ids[i],
            "metadata": metadatas[i],
            "document": documents[i]
        })
    
    return combined_results

@document_router.get('/')
def check_route():
    return "got route"