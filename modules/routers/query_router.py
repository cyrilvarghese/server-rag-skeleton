# query_router.py
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from modules.db import get_LC_chroma_client 
from modules.get_retriever import get_retriever  # Adjust the path accordingly
from modules.cross_encoder_rerank import get_reranked_docs

load_dotenv()
query_router = APIRouter()
router = APIRouter()

@query_router.post('/')
async def process_request(req_body: dict):
    try:
        question = req_body.get("question")
        num_of_results = int(req_body.get("results"))
        if not isinstance(question, str):
            raise HTTPException(status_code=400, detail='Invalid data format. Please provide an array of URLs and a question string.')

    
        retriever =get_retriever(num_of_results);       
        relevant_docs =   retriever.get_relevant_documents(question)
        print("Relevant docs  -----", len(relevant_docs))
        response = get_reranked_docs(question,relevant_docs)
        print("unique docs  -----", len(response))
        return response

    except Exception as e:
        print('Error processing request:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error.')

# Example usage:
# Create FastAPI instance and include this router
# app.include_router(router, prefix="/api/query")
