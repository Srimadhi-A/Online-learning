from flask import Flask, render_template, request, redirect, url_for
from models import db, UserProfile
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_profiles.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)

# Initialize DB on first request
@app.before_request
def create_tables():
    db.create_all()

# Allowed file extensions for images
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to create profile
@app.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        # Form data
        username = request.form['username']
        full_name = request.form['fullName']
        email = request.form['email']
        bio = request.form['bio']
        password = request.form['password']

        # Handle image upload
        profile_image = 'default-avatar.png'
        if 'profileImage' in request.files:
            image = request.files['profileImage']
            if image and allowed_file(image.filename):
                profile_image = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_image))

        # Create new user profile
        new_user = UserProfile(
            username=username,
            full_name=full_name,
            email=email,
            bio=bio,
            password=password,  # In production, hash the password
            profile_image=profile_image
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('profile', user_id=new_user.id))
        except Exception as e:
            db.session.rollback()
            return f"Error creating profile: {e}", 400

    return render_template('create_profile.html')

# Route to view the created profile
@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = UserProfile.query.get_or_404(user_id)

    # Fallback for missing profile image
    profile_image = user.profile_image if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], user.profile_image)) else 'default-avatar.png'

    return render_template(
        'profile.html',
        username=user.username,
        email=user.email,
        profile_image=profile_image
    )

if __name__ == "__main__":
    app.run(debug=True)
