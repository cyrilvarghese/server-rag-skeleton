from sentence_transformers import CrossEncoder


unique_contents = set()
unique_docs = []
pairs=[];
unique_content_details = []  # List to hold dictionaries of content details
files_folder = "files"  # Path to the 'files' folder
server_url = "http://localhost:8000"
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def get_reranked_docs(question,docs):
    """
    Extracts unique documents based on their page_content/reranks the docs as per relevance

    Args:
        docs (list): A nested list of documents.
        question: the query on the vector DB
        
    Returns:
       sorted array of documents
    """

    for doc in docs:
        if doc.page_content not in unique_contents:
                unique_contents.add(doc.page_content)
                unique_docs.append(doc)

  
    for content in unique_contents:
        # Extract the 'content' for scoring
        pairs.append([question, content])

    # Assume cross_encoder.predict() is a method that scores pairs of question and page_content
    scores = cross_encoder.predict(pairs)

    # # Immediately after scoring, print scores with URL source for verification
    # for score, content_detail in zip(scores, unique_content_details):
    #     print(f"Score: {score}, URL Source: {content_detail['url_source']}")

    # Combine the scores with the corresponding content details
    scored_docs = zip(scores, unique_docs)

    # Sort the combined list based on scores in descending order (higher scores are better)
    sorted_docs = sorted(scored_docs, reverse=True, key=lambda x: x[0])
    

    response = [item[1] for item in sorted_docs]
    return response