import os
# unique_docs.py
from urllib.parse import quote
from modules.helpers.cross_encoders import get_relevant_tags

def extract_unique_documents(docs):
    """
    Extracts unique documents based on their page_content from a nested list of documents and enriches
    the document with its original URL source if available.

    Args:
        docs (list): A nested list of documents.
        
    Returns:
        tuple: A tuple containing a list of unique documents and a list of dictionaries with detailed content information.
    """

    unique_contents = set()
    unique_docs = []
    unique_content_details = []  # List to hold dictionaries of content details
    files_folder = "files"  # Path to the 'files' folder
    server_url = "http://localhost:8000"

    for doc in docs:
        if doc.page_content not in unique_contents:
        

            tags = get_relevant_tags(doc.page_content)
            # Update doc metadata with URL source
            doc.metadata['tags'] = tags

            # Append the document to the list of unique documents
            unique_docs.append(doc)
            # Add the content's details to the unique_content_details list
            unique_content_details.append({
                "page_content": doc.page_content,
                "metadata":doc.metadata
            })

            # Add the page_content to the set of unique contents
            unique_contents.add(doc.page_content)
    
    return unique_docs, unique_content_details