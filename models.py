"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

def connect_db(app):
    """Connect database to Flask app."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """Blogy user."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable = False, default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return first and last name of user."""
        return f"{self.first_name} {self.last_name}"
    
  
    
class Post(db.Model):
    """Posts in Blogly."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return date"""
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")
    



############# Part 3 #########################

class Tag(db.Model):
    """Tag that can be added to posts"""
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    posts = db.relationship('Post', secondary="posts_tags", backref="tags")


class PostTag(db.Model):
    """Tag on a post"""
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key = True)

def connect_db(app):
    """Connect database to Flask app."""
    db.app = app
    db.init_app(app)