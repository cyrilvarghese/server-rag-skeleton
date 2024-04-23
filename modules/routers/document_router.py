# query_router.py
import json
from typing import List
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from modules.db import get_LC_chroma_client 
from modules.get_retriever import get_retriever  # Adjust the path accordingly
from modules.cross_encoder_rerank import get_reranked_docs
from sqlite_apis.data.model import Tag
from sqlite_apis.tags_router import list_tags

load_dotenv()
document_router = APIRouter()
all_tags = list_tags() 

@document_router.post('/')
async def get_chunks(req_body: dict):
    file_names = req_body.get("fileNames")
    if not file_names:
        raise HTTPException(status_code=400, detail="No file names provided.")

    results = []
    for file_name in file_names:
        try:
            result = filter_collection_by_metadata(file_name)
            results.append(({"file": file_name, "data": result}))
        except Exception as e:
            # Log the error and return a message specific to the error encountered
            print(f"Error processing file {file_name}: {str(e)}")
            results.append({"file": file_name, "error": "Failed to process due to an internal error"})

    return results

def filter_collection_by_metadata(file_name: str):
  
   
    print(f"Filtering collection for file: {file_name}")
    file_path= "../server/uploads/"+file_name;
     # filtering by source
    filtered_collection = get_LC_chroma_client().get(where={"source": file_path})
     # Adding tags by source
    results = combine_data_with_tags(filtered_collection["ids"],filtered_collection["metadatas"],filtered_collection["documents"],all_tags)
    # Simulate filtering logic
    return results
 
def parse_tag_names_and_scores(tag_data_str: str) -> List[dict]:
    # Assuming tag_data_str is a JSON string of tag data
    return json.loads(tag_data_str)

def find_tag_objects_with_scores(tag_data: List[dict], all_tags: List[dict]) -> List[Tag]:
    # Convert list of tag dicts to list of Tag models
    tag_objects = [Tag(**tag_dict) for tag_dict in all_tags]
    
    # Create a mapping of tag names to tag objects
    tag_map = {tag.name: tag for tag in tag_objects}

    # Attach scores to the tags and return them
    result_tags = []
    for tag_info in tag_data:
        tag_name = tag_info['tag_name']
        score = tag_info['score']
        if tag_name in tag_map:
            tag = tag_map[tag_name]
            tag.score = score  # Assign score to the tag
            result_tags.append(tag)
    
    return result_tags

def check_scores_review(tag_objects: List[Tag]) -> bool:
    # Check if any tag's score is less than -10
    return any(float(tag.score) < -10.00 for tag in tag_objects if tag.score is not None)

def combine_data_with_tags(ids, metadatas, documents, all_tags):
    combined_results = []

    if not (len(ids) == len(metadatas) == len(documents)):
        raise ValueError("The length of ids, metadatas, and documents must be the same.")
    
    for i in range(len(ids)):
        # Parse tag names and scores to get the list of tags with scores
        tag_data = parse_tag_names_and_scores(metadatas[i]['tags'])
        # Get the tag objects for the parsed tag data with scores
        tag_objects = find_tag_objects_with_scores(tag_data, all_tags)

        # Determine if the document needs review based on tag scores
        needs_review = check_scores_review(tag_objects)
        combined_results.append({
            "id": ids[i],
            "metadata": metadatas[i],
            "document": documents[i],
            "tags": tag_objects,  # Now includes score
            "review":needs_review
        })
    
    return combined_results

@document_router.post('/update_metadata')
async def update_metadata_tags(req_body: dict):
    try:
        # Convert these fields into lists if they are not already
        metadatas =  req_body.get('metadatas')
        ids =  req_body.get('doc_ids')

        # Get the client and perform the update asynchronously
        client = get_LC_chroma_client()
        client._collection.update(ids, metadatas)

        # Return a success message
        return {"message": "Metadata successfully updated", "updated_ids": ids}
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
 




@document_router.get('/')
def check_route():
    return "got route"