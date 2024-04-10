import sqlite3

db_path = '../server/sqlite_apis/data/singular-db.sqlite'
# Define the connection to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
def clear_all_data(conn, tables):
    cursor = conn.cursor()
    for table in tables:
        print(f"Clearing all data from {table}...")
        cursor.execute(f' DROP TABLE IF EXISTS {table};')
    conn.commit()
    print("All data cleared.\n")

# SQL statements to create the necessary tables
tables_creation_sql = [
    """
    CREATE TABLE IF NOT EXISTS Roles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        color TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        project_id INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES Projects(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Roles_Tags (
        role_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (role_id, tag_id),
        FOREIGN KEY (role_id) REFERENCES Roles(id),
        FOREIGN KEY (tag_id) REFERENCES Tags(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Projects_Tags (
        project_id INTEGER NOT NULL,
        tag_id INTEGER NOT NULL,
        PRIMARY KEY (project_id, tag_id),
        FOREIGN KEY (project_id) REFERENCES Projects(id),
        FOREIGN KEY (tag_id) REFERENCES Tags(id)
    );
    """,
    """
       CREATE TABLE IF NOT EXISTS Files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            project_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (job_id) REFERENCES Jobs(id),
            FOREIGN KEY (project_id) REFERENCES Projects(id)
        );
    """
]
# List of table names to clear and seed
tables = ['Roles', 'Tags', 'Projects', 'Jobs', 'Roles_Tags', 'Projects_Tags','Files']

# Clear all data from tables before seeding
clear_all_data(conn, tables)
# Execute each SQL statement
for create_table_sql in tables_creation_sql:
    cursor.execute(create_table_sql)

# Commit the changes and close the connection
conn.commit()
conn.close()
print("tables created in 'singular_db.sqlite'  successfully.")
