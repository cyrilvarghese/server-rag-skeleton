from dotenv import load_dotenv
from config import DB_NAME, BASE_PATH
import chromadb
import os
from modules.file_processor_with_indexing import process_files
load_dotenv()
 
def clear_processed_files():
    try:
        os.remove(BASE_PATH+"/utils/processed_files.txt")
        print("Processed files cleared successfully.")
    except FileNotFoundError:
        print("Processed files not found. No action taken.")

from chromadb.config import Settings
async def setup_chroma(is_reset=False):
    try:    
    #    chroma db client not langchain for resetting 
        chroma_client = chromadb.HttpClient(host='localhost', port=3001)

        
        if is_reset:
             print("client Reset ",chroma_client.reset());
        collection = chroma_client.get_or_create_collection(name=DB_NAME)
        print("collection created - count:",collection.count())
        if is_reset:
            clear_processed_files()
            await process_files()
    except Exception as e:
        print("An error occurred:", str(e))
    
 