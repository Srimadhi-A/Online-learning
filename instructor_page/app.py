from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure the file upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')  # Absolute path
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Function to check if the file is a valid image
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Database path
db_path = os.path.join(os.path.dirname(__file__), 'database.db')

# Ensure the database exists
if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Create the tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instructor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        biography TEXT,
        image_url TEXT,
        contact_email TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        instructor_id INTEGER NOT NULL,
        course_name TEXT NOT NULL,
        FOREIGN KEY (instructor_id) REFERENCES instructor (id)
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('instructor_signup.html')  # Home page or index page

@app.route('/become-instructor', methods=['GET'])
def become_instructor():
    return render_template('instructor_signup.html')

@app.route('/submit-instructor', methods=['POST'])
def submit_instructor():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        biography = request.form['biography']
        contact_email = request.form['contact_email']

        # Handle profile image upload
        image = request.files.get('image')
        image_filename = None

        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            # Ensure the directory exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))

        # Insert data into the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(''' 
        INSERT INTO instructor (name, biography, image_url, contact_email)
        VALUES (?, ?, ?, ?)
        ''', (name, biography, image_filename, contact_email))

        conn.commit()
        conn.close()

        return redirect(url_for('home'))

@app.route('/instructor', methods=['GET'])
def instructor():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve instructor data (assuming ID = 1 for demo purposes)
    cursor.execute("SELECT * FROM instructor WHERE id = 1")
    instructor = cursor.fetchone()

    # Retrieve courses taught by the instructor
    cursor.execute("SELECT * FROM courses WHERE instructor_id = 1")
    courses = cursor.fetchall()

    conn.close()

    # If no instructor is found, show a friendly message or redirect
    if not instructor:
        return render_template('instructor_page.html', instructor=instructor, courses=[])

    return render_template('instructor_page.html', instructor=instructor, courses=courses)


# Route to test the database connection
@app.route('/test-db', methods=['GET'])
def test_db():
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
        conn.close()
        return "Database connection successful"
    except sqlite3.Error as e:
        return f"Database connection failed: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
