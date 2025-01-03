from flask import Flask, request, jsonify, render_template, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            bio TEXT,
            profile_pic TEXT DEFAULT 'default.png'
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def profile_page():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, bio, profile_pic FROM users WHERE id=1")
    user = cursor.fetchone()
    conn.close()

    if user:
        username, email, bio, profile_pic = user
        profile_pic_url = url_for('static', filename=f'uploads/{profile_pic}')
    else:
        username, email, bio, profile_pic_url = "", "", "", url_for('static', filename='uploads/default.png')

    return render_template("index.html", username=username, email=email, bio=bio, profile_pic_url=profile_pic_url)

@app.route("/update_profile", methods=["POST"])
def update_profile():
    username = request.form.get("username")
    email = request.form.get("email")
    bio = request.form.get("bio")
    profile_picture = request.files.get("profilePicture")

    profile_pic_filename = None
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        profile_pic_filename = f"{email}_{filename}"
        profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic_filename))

    try:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Update user details and profile picture if provided
        if profile_pic_filename:
            cursor.execute("""
                INSERT INTO users (username, email, bio, profile_pic)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                username=excluded.username, bio=excluded.bio, profile_pic=excluded.profile_pic
            """, (username, email, bio, profile_pic_filename))
        else:
            cursor.execute("""
                INSERT INTO users (username, email, bio)
                VALUES (?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                username=excluded.username, bio=excluded.bio
            """, (username, email, bio))

        conn.commit()
        conn.close()

        profile_pic_url = url_for('static', filename=f'uploads/{profile_pic_filename}') if profile_pic_filename else None
        return jsonify({"success": True, "profile_pic_url": profile_pic_url})

    except Exception as e:
        print(e)
        return jsonify({"success": False})

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
