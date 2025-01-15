import sqlite3
import os

# Set the absolute path for the database file
db_dir = os.path.join('D:', 'html', 'Online-learning-main', 'instructor_page')  # Absolute path to the folder
db_path = os.path.join(db_dir, 'database.db')

# Ensure the directory exists
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Create the database file and establish a connection
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the 'instructor' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS instructor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    biography TEXT NOT NULL,
    image_url TEXT,
    contact_email TEXT NOT NULL
)
''')

# Create the 'courses' table (assuming you need it)
cursor.execute('''
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_id INTEGER,
    course_name TEXT NOT NULL,
    course_description TEXT,
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
)
''')

conn.commit()
conn.close()

print("Database and tables created successfully!")
