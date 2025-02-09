from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(500))
    password = db.Column(db.String(200), nullable=False)
    profile_image = db.Column(db.String(200), default='default-avatar.png')  # Image path
    
    def __repr__(self):
        return f"<UserProfile {self.username}>"
