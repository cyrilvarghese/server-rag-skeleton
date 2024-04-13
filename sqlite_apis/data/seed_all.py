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
                ('Tagging Financial Report First Draft', 1, '2023-11-28 04:08:37'),
                ('Tagging Financial Report Revised Draft', 1, '2023-12-15 04:08:37'),
                ('Tagging Financial Report Final Draft', 1, '2023-12-12 04:08:37'),
                ('Tagging Financial Report Executive Summary', 1, '2023-12-25 04:08:37'),
                ('Tagging Latest Edited Financial Report', 1, '2023-11-10 04:08:37'),
                ('Tagging HR Report Initial Draft', 2, '2023-11-28 04:08:37'),
                ('Tagging HR Report Mid-Year Review', 2, '2023-10-31 04:08:37'),
                ('Tagging HR Report Year-End Summary', 2, '2023-12-15 04:08:37'),
                ('Tagging HR Report Detailed Analysis', 2, '2023-10-27 04:08:37'),
                ('Tagging Latest HR Report Updates', 2, '2023-12-12 04:08:37'),
                ('Tagging Performance Report Q1 Review', 3, '2023-12-25 04:08:37'),
                ('Tagging Performance Report Q2 Insights', 3, '2023-11-20 04:08:37'),
                ('Tagging Performance Report Q3 Summary', 3, '2023-11-10 04:08:37'),
                ('Tagging Performance Report Annual Review', 3, '2024-03-26 04:08:37'),
                ('Tagging Latest Performance Insights', 3, '2023-11-09 04:08:37'),
                ('Tagging Executive Summary First Draft', 1, '2023-12-29 04:08:37'),
                ('Tagging Executive Summary Revised Draft', 1, '2024-03-12 04:08:37'),
                ('Tagging Executive Summary Final Draft', 1, '2024-03-27 04:08:37'),
                ('Tagging Executive Summary Detailed Review', 1, '2024-01-03 04:08:37')
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
        (1, 1, 'Financial_Report_First_Draft_1.pdf', '2023-11-15 04:08:37'),
        (2, 1, 'Financial_Report_Revised_Draft_1.pdf', '2024-04-07 04:08:37'),
        (2, 1, 'Financial_Report_Revised_Draft_2.pdf', '2024-01-24 04:08:37'),
        (3, 1, 'Financial_Report_Final_Draft_1.pdf', '2023-11-04 04:08:37'),
        (3, 1, 'Financial_Report_Final_Draft_2.pdf', '2024-01-18 04:08:37'),
        (4, 1, 'Financial_Report_Executive_Summary_1.pdf', '2024-03-18 04:08:37'),
        (5, 1, 'Latest_Edited_Financial_Report_1.pdf', '2024-03-11 04:08:37'),
        (5, 1, 'Latest_Edited_Financial_Report_2.pdf', '2024-02-07 04:08:37'),
        (6, 1, 'HR_Report_Initial_Draft_1.pdf', '2024-02-03 04:08:37'),
        (7, 1, 'HR_Report_Mid_Year_Review_1.pdf', '2024-01-21 04:08:37'),
        (8, 1, 'HR_Report_Year_End_Summary_1.pdf', '2024-04-02 04:08:37'),
        (8, 1, 'HR_Report_Year_End_Summary_2.pdf', '2023-11-17 04:08:37'),
        (9, 1, 'HR_Report_Detailed_Analysis_1.pdf', '2023-10-20 04:08:37'),
        (10, 1, 'Latest_HR_Report_Updates_1.pdf', '2023-11-16 04:08:37'),
        (10, 1, 'Latest_HR_Report_Updates_2.pdf', '2023-11-22 04:08:37'),
        (11, 1, 'Performance_Report_Q1_Review_1.pdf', '2024-03-12 04:08:37'),
        (12, 1, 'Performance_Report_Q2_Insights_1.pdf', '2024-03-28 04:08:37'),
        (13, 1, 'Performance_Report_Q3_Summary_1.pdf', '2024-03-16 04:08:37'),
        (14, 1, 'Performance_Report_Annual_Review_1.pdf', '2024-02-29 04:08:37'),
        (15, 1, 'Latest_Performance_Insights_1.pdf', '2024-02-28 04:08:37'),
        (16, 1, 'Executive_Summary_First_Draft_1.pdf', '2024-01-29 04:08:37'),
        (16, 1, 'Executive_Summary_First_Draft_2.pdf', '2024-02-02 04:08:37'),
        (17, 1, 'Executive_Summary_Revised_Draft_1.pdf', '2024-02-16 04:08:37'),
        (17, 1, 'Executive_Summary_Revised_Draft_2.pdf', '2023-11-19 04:08:37'),
        (18, 1, 'Executive_Summary_Final_Draft_1.pdf', '2024-03-05 04:08:37'),
        (18, 1, 'Executive_Summary_Final_Draft_2.pdf', '2024-03-06 04:08:37'),
        (19, 1, 'Executive_Summary_Detailed_Review_1.pdf', '2023-12-25 04:08:37'),
        (19, 1, 'Executive_Summary_Detailed_Review_2.pdf', '2023-12-26 04:08:37')
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
