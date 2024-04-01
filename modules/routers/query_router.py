# query_router.py
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from modules.db import get_LC_chroma_client 
load_dotenv()
query_router = APIRouter()
router = APIRouter()

@query_router.get('/')
async def process_request():
    try:
        # Extracting text from each tuple item
        collection = get_LC_chroma_client().get();
       
        # text_array = [doc.page_content for doc in sorted_docs]
        return collection

    except Exception as e:
        print('Error processing request:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error.')

# Example usage:
# Create FastAPI instance and include this router
# app.include_router(router, prefix="/api/query")
