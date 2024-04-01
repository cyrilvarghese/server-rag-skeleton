from dotenv import load_dotenv
from config import DB_NAME, DB_URL
import chromadb
import os

# Set environment variables
os.environ['ALLOW_RESET'] = 'True'

load_dotenv()
from chromadb.config import Settings
async def setup_chroma(is_reset=False):
    try:    
        chroma_client = chromadb.HttpClient(host='localhost', port=3001)
        if is_reset:
             print("client Reset ",chroma_client.reset());
        collection = chroma_client.create_collection(name=DB_NAME)
        print("collection created - count:",collection.count())
    except Exception as e:
        print("An error occurred:", str(e))
    
 