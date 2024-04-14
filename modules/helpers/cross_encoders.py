
from sentence_transformers import CrossEncoder
import json
from config import BASE_PATH
from sqlite_apis.tags_router import list_tags

def get_relevant_tags(document: str):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    tags = list_tags()  # Use your custom function to get tags

    pairs = []
    relevant_tags = []

    # Loop through the list of tag descriptions
    for tag in tags:
        # Access the tag_name and tag_description for each tag
        tag_name = tag['name']  # Adjusted for database keys
        tag_description = tag['description']  # Adjusted for database keys

        print(f"Tag Name: {tag_name}\nDescription: {tag_description}\n")

        pairs.append([tag_description, document])

    # Score pairs of question and page_content
    scores = cross_encoder.predict(pairs)

    # Print scores with URL source for verification
    for score, tag in zip(scores, tags):
        print(f"Score: {score}, Tag Name: {tag['name']}")  # Adjusted for database keys

    # Combine the scores with the corresponding tags
    scored_tags = zip(scores, tags)

    # Sort the combined list based on scores in descending order (higher scores are better)
    sorted_tags = sorted(scored_tags, reverse=True, key=lambda x: x[0])
    print(sorted_tags)

    # Retrieve relevant tags based on a threshold
    relevant_tags = get_with_threshold(sorted_tags)

    # Metadata in chroma cannot have list so converting to strings
    relevant_tags_str = json.dumps(relevant_tags)
    return relevant_tags_str


def get_with_threshold(data, threshold_value=1):
    max_score = max(data, key=lambda x: x[0])[0]
    threshold_range = max_score - threshold_value
    relevant_tag_names = []
    for score, tag_info in data:
        if score >= threshold_range:
            relevant_tag_names.append(tag_info['name'])  # Adjusted for database keys
    return relevant_tag_names