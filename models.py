"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = "users"
    
    # username - a unique primary key that is no longer than 20 characters.
    username = db.Column(db.String(20), unique=True, primary_key=True)
    # password - a not-nullable column that is text
    password = db.Column(db.Text, nullable=False)
    # email - a not-nullable column that is unique and no longer than 50 characters.
    email = db.Column(db.String(50), unique=True, nullable=False)
    # first_name - a not-nullable column that is no longer than 30 characters.
    first_name = db.Column(db.String(30), nullable=False)
    # last_name - a not-nullable column that is no longer than 30 characters.
    last_name = db.Column(db.String(30), nullable=False)
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        u = User.query.get(username)
        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
        
    feedbacks = db.relationship('Feedback', backref='user', cascade="all, delete-orphan")
    
class Feedback(db.Model):
    __tablename__ = "feedbacks"
    
    # id - a unique primary key that is an auto incrementing integer
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # title - a not-nullable column that is at most 100 characters
    title = db.Column(db.String(100), nullable=False)
    # content - a not-nullable column that is text
    content = db.Column(db.Text, nullable=False)
    # username - a foreign key that references the username column in the users table
    username = db.Column(db.String(20), db.ForeignKey('users.username'))
    