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
        # print(f"Tag Name: {tag_name}\nDescription: {tag_description}\n")

        pairs.append([tag_description, document])

      # Score pairs of tag description and document
    scores = cross_encoder.predict(pairs)

    # Print scores with URL source for verification
    for score, tag in zip(scores, tags):
        print(f"Score: {score}, Tag Name: {tag['name']}")  # Adjusted for database keys

    # Combine the scores with the corresponding tags
    scored_tags = list(zip(scores, tags))

    # Sort the list based on scores in descending order (higher scores are better)
    sorted_tag_scores = sorted(scored_tags, key=lambda x: x[0], reverse=True)

    # Get the top three tags
    top_three_tags = sorted_tag_scores[:3]

    # Convert top three tags into a list of dictionaries with tag name and score
    top_three_tags_formatted = [{"tag_name": tag['name'], "score": str(score)} for score, tag in top_three_tags]
    print(top_three_tags_formatted)

    # Assuming the output needs to be in JSON format
    return json.dumps(top_three_tags_formatted)


# def get_with_threshold(data, threshold_value=1):
#     max_score = max(data, key=lambda x: x[0])[0]
#     threshold_range = max_score - threshold_value
#     relevant_tag_names = []
#     for score, tag_info in data:
#         if score >= threshold_range:
#             relevant_tag_names.append(tag_info['name'])  # Adjusted for database keys
#     return relevant_tag_names
 