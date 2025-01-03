from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Mock data for courses
courses = [
    {"id": 1, "name": "Python for Beginners", "description": "Learn Python basics.", "enrolled": False},
    {"id": 2, "name": "HTML & CSS Basics", "description": "Master HTML and CSS.", "enrolled": False},
    {"id": 3, "name": "JavaScript Essentials", "description": "Learn JavaScript fundamentals.", "enrolled": False}
]

# Route to get available courses
@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(courses)

# Route to enroll in a course
@app.route('/enroll', methods=['POST'])
def enroll_course():
    data = request.get_json()
    course_id = data.get("course_id")

    for course in courses:
        if course["id"] == course_id:
            course["enrolled"] = True
            return jsonify({"message": f"Successfully enrolled in {course['name']}!"}), 200

    return jsonify({"message": "Course not found!"}), 404

if __name__ == '__main__':
    app.run(debug=True)
