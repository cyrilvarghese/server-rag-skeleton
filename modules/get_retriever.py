from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
load_dotenv()
from modules.db import get_LC_chroma_client
from config import DB_NAME


 
def get_retriever(num_of_results=20):
    try:
        collection = get_LC_chroma_client.get_collection(name=DB_NAME)
        print("---from api")
        print(collection)
        if collection:
            retriever = get_LC_chroma_client.as_retriever( search_kwargs={"k": num_of_results})
            return retriever
    except Exception as e:
        print('Error retrieving documents:', e)

# Example usage:
# retriever = await get_retriever()
# relevant_docs = await retriever.get_relevant_documents(question)