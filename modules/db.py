# db.py
import chromadb
from chromadb import Settings
from config import DB_NAME
from  langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Global variable to hold the persistent client instance
# persistent_client = None

# def get_db(is_reset=False):
#     global persistent_client
#     if persistent_client is None:
#         persistent_client = chromadb.PersistentClient(
#             path="chroma_db",
#             settings=Settings(allow_reset=is_reset)
#         )
#     return persistent_client

def get_LC_chroma_client():
    chroma_client = chromadb.HttpClient(host='localhost', port=3001)
    embeddings = OpenAIEmbeddings(model= "text-embedding-3-large")

    langchain_chroma = Chroma(
        client=chroma_client,
        collection_name=DB_NAME,
        embedding_function=embeddings,
    )
    return langchain_chroma


