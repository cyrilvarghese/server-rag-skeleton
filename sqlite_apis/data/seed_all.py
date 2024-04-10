import sqlite3
from datetime import datetime
db_path = '../server/sqlite_apis/data/singular-db.sqlite'


def seed_table(conn, table_name, data, columns=None):
    cursor = conn.cursor()
    if columns:
        placeholders = ', '.join('?' for _ in data[0])
        columns_string = ', '.join(columns)
        sql = f'INSERT INTO {table_name} ({columns_string}) VALUES ({placeholders})'
    else:
        placeholders = ', '.join('?' for _ in data[0])
        sql = f'INSERT INTO {table_name} VALUES (NULL, {placeholders})'
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
  

    # Sample data for the Roles table
    roles_data = [
        ('Administrator', 'Full access to the system'),
        ('Editor', 'Can publish articles, but not delete them'),
        ('Contributor', 'Can write articles, but not publish them'),
        ('Moderator', 'Can moderate comments'),
        ('Viewer', 'Can view content, read-only access')
    ]

    # Sample data for the Projects table
    projects_data = [
        ('Financial Report Document', 'Project for tagging different versions of financial reports.'),
        ('HR Report Document', 'Project for tagging different versions of HR reports.'),
        ('Performace Report Document', 'Project for tagging different versions of Performace reports.')
    ]

    # Sample data for the Jobs table
    jobs_data = [
        ('Tagging Financial Report First Draft', 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('Tagging Latest Edited Financial Report', 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('Tagging Financial Report Revised Draft', 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('Tagging Financial Report Final Draft', 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        ('Tagging Financial Report Executive Summary', 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]

    # Sample data for the Tags table
    tags_data = [
        ('Strategic', 'Related to strategic overview', '#FFD700'),
        ('Operational', 'Pertains to operations management', '#007FFF'),
        ('Financial', 'Involves financial data and statistics', '#20B2AA'),
        ('Regulatory', 'Concerns regulatory compliance', '#DAA520'),
        ('HR', 'Relates to human resources', '#708090')
    ]
    
    # Assuming we have the following structure for 'Roles_Tags' and 'Projects_Tags' junction tables
    # We will randomly associate roles and projects with tags for the sake of this example
  # Sample data for Roles_Tags (associating 1 to 3 tags with each role)
    roles_tags_data = [
        (1, 1), (1, 2),  # Role 1 associated with Tag 1 and Tag 2
        (2, 1), (2, 3),  # Role 2 associated with Tag 1 and Tag 3
        (3, 2),         # Role 3 associated with Tag 2
        (4, 3), (4, 4),  # Role 4 associated with Tag 3 and Tag 4
        (5, 5)           # Role 5 associated with Tag 5
    ]

    # Sample data for Projects_Tags (associating 5 tags with Project 1)
    projects_tags_data = [
        (1, 1),
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5)
    ]

    # Seed data for the 'Files' table, with each file mapped to a specific job_id.
    # We will use job_ids 1 to 5 for the purpose of this example. In practice, these should exist in your 'Jobs' table.
    files_data = [
        (1,1, 'Financial Report Q1.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (1,1, 'Financial Report Q2.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2,1, 'Marketing Plan Q1.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (2,1, 'Marketing Plan Q2.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3,1, 'Product Roadmap 2024.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (3,1, 'Product Launch Details.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (4,1, 'Q3 Budget Review.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5,1, 'Q4 Forecast.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        (5,1, 'End of Year Report.pdf', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    ]


    # Seed the Roles table
    seed_table(conn, 'Roles', roles_data)

    # Seed the Projects table
    seed_table(conn, 'Projects', projects_data)

    # Seed the Jobs table
    seed_table(conn, 'Jobs', jobs_data, ['name', 'project_id', 'created_at'])

    # Seed the Tags table
    seed_table(conn, 'Tags', tags_data, ['name', 'description','color'])
    seed_table(conn, 'Roles_Tags', roles_tags_data, ['role_id', 'tag_id'])
    seed_table(conn, 'Projects_Tags', projects_tags_data, ['project_id', 'tag_id'])
    seed_table(conn, 'Files', files_data, ['job_id','project_id', 'name',"created_at"])

    print("Database 'singular_db.sqlite' has been successfully seeded with sample data.")

if __name__ == "__main__":
    main()
