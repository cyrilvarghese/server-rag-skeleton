import sqlite3
import json

# Path to your SQLite database
db_path = '../server/sqlite_apis/data/singular-db.sqlite'
# Path to your JSON file with the tag data
json_file_path = '../server/sqlite_apis/data/tag_description_mapping.json'

def seed_tags(db_path, json_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Open and read the JSON file
    with open(json_file_path, 'r') as file:
        tags = json.load(file)
    
    # Insert each tag into the database
    for tag in tags:
        cursor.execute('INSERT INTO Tags (name, description) VALUES (?, ?)',
                       (tag['tag_name'], tag['tag_description']))
    
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

# Run the seeding function
seed_tags(db_path, json_file_path)

print("Database seeded successfully with tags.")
