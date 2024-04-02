
from sentence_transformers import CrossEncoder
import json
from config import BASE_PATH

# Load the JSON data from the file
with open(BASE_PATH+'/uploads/tag_description_mapping.json', 'r') as file:
    tag_descriptions = json.load(file)


def get_relevant_tags(document:str):
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
    pairs = []
    relevant_tags=[]
  # Loop through the list of tag descriptions
    for tag in tag_descriptions:
        # Access the tag_name and tag_description for each tag
        tag_name = tag['tag_name']
        tag_description = tag['tag_description']
           
        print(f"Tag Name: {tag_name}\nDescription: {tag_description}\n")

        pairs.append([tag_description, document])

    # Assume cross_encoder.predict() is a method that scores pairs of question and page_content
    scores = cross_encoder.predict(pairs)

    # Immediately after scoring, print scores with URL source for verification
    for score, tag  in zip(scores, tag_descriptions):
        print(f"Score: {score}, Tag Name: {tag['tag_name']}")

    # Combine the scores with the corresponding tag_descriptions
    scored_tags = zip(scores, tag_descriptions)

    # Sort the combined list based on scores in descending order (higher scores are better)
    sorted_tags = sorted(scored_tags, reverse=True, key=lambda x: x[0])
    print(sorted_tags)
    # Initialize an empty list to hold the tag_names

    relevant_tags = get_with_threshold(sorted_tags)

    #metadata in chroma cannot have list so converting to strtings
    relevant_tags_str = json.dumps(relevant_tags)
    return relevant_tags_str


def get_with_threshold(data, threshold_value=3):
    max_score = max(data, key=lambda x: x[0])[0]
    threshold_range = max_score - threshold_value
    relevant_tag_names = []
    for score, tag_info in data:
        if score >= threshold_range:
            relevant_tag_names.append(tag_info['tag_name'])
    return relevant_tag_names