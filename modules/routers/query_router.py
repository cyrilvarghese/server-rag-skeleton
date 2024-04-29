# query_router.py
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from modules.db import get_LC_chroma_client 
from modules.get_retriever import get_retriever  # Adjust the path accordingly
from modules.cross_encoder_rerank import get_reranked_docs

load_dotenv()
query_router = APIRouter()
 

@query_router.post('/')
async def process_request(req_body: dict):
    try:
        question = req_body.get("question")
        file_names = req_body.get("file_names")
        # num_of_results = int(req_body.get("results"))
        if not isinstance(question, str):
            raise HTTPException(status_code=400, detail='Invalid data format. Please provide an array of URLs and a question string.')

        # retriever =get_retriever(num_of_results);       
        # relevant_docs =   retriever.get_relevant_documents(question)
        print(f"Filtering collection for {len(file_names)} files")
      
        file_paths = ["../server/uploads/" + file_name for file_name in file_names]
        LC_chroma_client=get_LC_chroma_client();
        retriever=LC_chroma_client.as_retriever(
                        search_kwargs={ "filter":{'source': {'$in': file_paths}}}
                    )
      
        relevant_docs =   retriever.invoke(question)
        print("Relevant docs  -----", len(relevant_docs))
        if len(relevant_docs)>0:
            response = get_reranked_docs(question,relevant_docs)
            print("unique docs  -----", len(response))
            return response

    except Exception as e:
        print('Error processing request:', e)
        raise HTTPException(status_code=500, detail='Internal Server Error.')

# Example usage:
# Create FastAPI instance and include this router
# app.include_router(router, prefix="/api/query")
 