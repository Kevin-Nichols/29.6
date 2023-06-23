"""Models for web site"""
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    app.app_context().push()


class User(db.Model):
    """Model for new site user."""
    __tablename__ = 'users'
    
    username = db.Column(db.String(20),
                        nullable=False,
                        unique=True,
                        primary_key=True)
    password = db.Column(db.Text,
                         nullable=False)
    email = db.Column(db.String(50),
                         nullable=False,
                         unique=True)
    first_name = db.Column(db.String(30),
                         nullable=False)
    last_name = db.Column(db.String(30),
                         nullable=False)
    
    feedback = db.relationship('Feedback', backref='user', cascade='all,delete')
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Hashes a password for registering a new user."""
        hashed = bcrypt.generate_password_hash(pwd)
        
        hashed_utf8 = hashed.decode('utf8')
        
        new_user = cls(username=username, 
                       password=hashed_utf8,
                       email=email,
                       first_name=first_name,
                       last_name=last_name)

        return new_user
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validates that a user is in the database and password matches."""
        u = User.query.filter_by(username=username).first()
        
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
        
        
class Feedback(db.Model):
    """Model for new feedback."""
    __tablename__ = "feedback"

    id = db.Column(db.Integer, 
                   primary_key=True)
    title = db.Column(db.String(100), 
                      nullable=False)
    content = db.Column(db.Text, 
                        nullable=False)
    username = db.Column(db.String(20), 
                         db.ForeignKey('users.username'), 
                         nullable=False,)