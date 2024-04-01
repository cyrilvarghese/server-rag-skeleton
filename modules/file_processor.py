# file_processor.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from  langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE
from modules.db import get_LC_chroma_client

 
# Initialize list to store documents
documents = []
splitter =  RecursiveCharacterTextSplitter(
                # Set a really small chunk size, just to show.
                chunk_size=CHUNK_SIZE,

            )



async def process_files(folder_path="../server/uploads", processed_files_path="../server/utils/processed_files.txt"):
    try:
        # Read the list of processed files
        processed_files = read_processed_files(processed_files_path)
        
        files = os.listdir(folder_path)

        for file in files:
            file_path = os.path.join(folder_path, file)
            
            # Skip processing if the file has already been processed
            if file in processed_files:
                print(f"Skipping {file_path}. Already processed.")
                continue
            
            file_type = get_file_type(file_path)

            if file_type == "txt" and ("urls.txt" and "processed_files.txt") not in file:
                get_text_loader(file_path,file)
            elif file_type == "pdf":
                get_pdf_loader(file_path,file)
            else:
                print(f"Unsupported file type for {file_path}")

        # Update the list of processed files
        update_processed_files(processed_files_path, files)
        
        #flatten array of arrays
        docs_to_index = []
        for array in documents:
            docs_to_index.extend(array)
 
         
            
        print("Document count:", len(docs_to_index))
        print("Adding docs...")

        # db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
        langchain_chroma = get_LC_chroma_client()
        # Create vector store
        return await langchain_chroma.aadd_documents(documents=docs_to_index)
    except Exception as e:
        print('Error processing files:', e)

def read_processed_files(file_path):
    try:
        with open(file_path, "r") as file:
            processed_files = [line.strip() for line in file]
        return processed_files
    except FileNotFoundError:
        print(f"no file {file_path}. Starting fresh.")
        return []

def update_processed_files(file_path, processed_files):
    try:
        with open(file_path, "w") as file:
            for file_name in processed_files:
                file.write(file_name + "\n")
        print(f"updated {file_path}")
    except Exception as e:
        print(f"Error updating processed files at {file_path}: {e}")


# Function to determine the file type based on extension
def get_file_type(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext[1:]  # Removing the dot from the extension

# Function for handling txt files
def get_text_loader(file_path,file):
    print(f"spilting file: {file}")
    text_loader = TextLoader(file_path)
    docs_text =  text_loader.load()
    docs =  splitter.split_documents(docs_text)
    documents.append(docs)
    

# Function for handling pdf files
def get_pdf_loader(file_path,file):
    print(f"spilting file: {file}")
    pdf_loader = PyPDFLoader(file_path)
    docs_pdf =  pdf_loader.load()
    docs =  splitter.split_documents(docs_pdf)
    documents.append(docs)
    

