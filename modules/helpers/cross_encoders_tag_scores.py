from sentence_transformers import CrossEncoder
import json

# Assuming get_list is defined elsewhere and imports the necessary database connection
from sqlite_apis.tags_router import list_tags
 

def get_relevant_tags(document: str,threshold_value=1.0):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    tags = list_tags()  # Use your custom function to get tags

    pairs = []
    relevant_tags = []

    # Loop through the list of tag descriptions
    for tag in tags:
        # Access the tag_name and tag_description for each tag
        tag_name = tag['name']
        tag_description = tag['description']
        print(f"Tag Name: {tag_name}\nDescription: {tag_description}\n")

        pairs.append([tag_description, document])

    # Score pairs of tag description and document
    scores = cross_encoder.predict(pairs)

    # Print scores with URL source for verification
    for score, tag in zip(scores, tags):
        print(f"Score: {score}, Tag Name: {tag['name']}")  # Adjusted for database keys

    # Combine the scores with the corresponding tags
    scored_tags = list(zip(scores, tags))
    
    # Calculate the maximum score to set up a threshold
    max_score = max(scored_tags, key=lambda x: x[0])[0]
    threshold_range = max_score - threshold_value

    # Filter tags that meet the threshold creating tag name / score object array
    filtered_tags = [{"tag_name": tag['name'], "score": str(score)} for score, tag in scored_tags if score >= threshold_range]
 
    # Sort the list based on scores in descending order (higher scores are better)
    sorted_tag_scores = sorted(filtered_tags, key=lambda x: float(x["score"]), reverse=True)
    print(sorted_tag_scores)

    return json.dumps(sorted_tag_scores)


def get_with_threshold(data, threshold_value=1):
    max_score = max(data, key=lambda x: x[0])[0]
    threshold_range = max_score - threshold_value
    relevant_tag_names = []
    for score, tag_info in data:
        if score >= threshold_range:
            relevant_tag_names.append(tag_info['name'])  # Adjusted for database keys
    return relevant_tag_names
 