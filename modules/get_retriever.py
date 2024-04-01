from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
load_dotenv()
from modules.db import get_db
from config import DB_NAME

embeddings = OpenAIEmbeddings(model= "text-embedding-3-large")
# embeddings = CohereEmbeddings(model="embed-english-light-v3.0")
chroma_client = chromadb.HttpClient(host='localhost', port=3001)

 
def get_retriever(num_of_results):
    try:
        collection = chroma_client.get_collection(name=DB_NAME)
        print("---from api")
        print(collection)
        if collection:
            # persistent_client = chromadb.PersistentClient(path="chroma_db",settings=Settings(allow_reset=True))
            persistent_client = get_db();
            langchain_chroma= Chroma(client=persistent_client, embedding_function=embeddings,collection_name="ux-research-base")
            # retriever = langchain_chroma.as_retriever(  search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.5,"k": num_of_results})
            retriever = langchain_chroma.as_retriever( search_kwargs={"k": num_of_results})
    
            return retriever
    except Exception as e:
        print('Error retrieving documents:', e)

# Example usage:
# retriever = await get_retriever()
# relevant_docs = await retriever.get_relevant_documents(question)