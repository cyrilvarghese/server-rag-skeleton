# file_processor.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from  langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE,UPLOADS_FOLDER
from modules.db import get_LC_chroma_client
from modules.helpers.cross_encoders_tag_scores import get_relevant_tags
from datetime import datetime
from langchain.indexes import SQLRecordManager, index
from langchain_core.documents import Document
from config import DB_NAME as collection_name

# Initialize list to store documents
 
splitter =  RecursiveCharacterTextSplitter(
                # Set a really small chunk size, just to show.
                chunk_size=CHUNK_SIZE,

            )
namespace = f"chromadb/{collection_name}"
record_manager = SQLRecordManager(
    namespace, db_url="sqlite:///record_manager_cache.sql"
)
record_manager.create_schema()


async def process_files(folder_path=UPLOADS_FOLDER):
    documents = []
    try:
          
        files = os.listdir(folder_path)

        for file in files:
            file_path = os.path.join(folder_path, file)
            
            file_type = get_file_type(file_path)

            if file_type == "txt" and ("urls.txt" and "processed_files.txt") not in file:
                get_text_loader(file_path,file,documents)
            elif file_type == "pdf":
                get_pdf_loader(file_path,file,documents)
            else:
                print(f"Unsupported file type for {file_path}")

        
        #flatten array of arrays
      
        docs_to_index = []
        for array in documents:
            docs_to_index.extend(array)
      
    #   adding meta info for querying 
        for doc in docs_to_index:
            tags = get_relevant_tags(doc.page_content)
            # Update doc metadata with tags
            doc.metadata['tags'] = tags
            # doc.metadata['created_at'] =  datetime.now().isoformat()
            # doc.metadata['updated_at'] =  datetime.now().isoformat()
         
            
        print("Document count:", len(docs_to_index))
        print("Adding docs...")

        langchain_chroma = get_LC_chroma_client()

        response = index(
            docs_to_index,
            record_manager,
            langchain_chroma,
            cleanup="incremental",
            source_id_key="source",
        )

        print(response)
        # Create vector store
        return response
    except Exception as e:
        print('Error processing files:', e)



# Function to determine the file type based on extension
def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext[1:]  # Removing the dot from the extension

# Function for handling txt files
def get_text_loader(file_path,file,documents):
    print(f"spilting file: {file}")
    text_loader = TextLoader(file_path)
    docs_text =  text_loader.load()
    docs =  splitter.split_documents(docs_text)
    documents.append(docs)
    

# Function for handling pdf files
def get_pdf_loader(file_path,file,documents):
    print(f"spilting file: {file}")
    pdf_loader = PyPDFLoader(file_path)
    docs_pdf =  pdf_loader.load()
    docs =  splitter.split_documents(docs_pdf)
    documents.append(docs)
    

