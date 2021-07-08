"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String, nullable=True)

    # QUESTION: HOW TO DELETE DEPENDENCIES
    posts = db.relationship('Post', backref="users", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} >"

class Post(db.Model):
    """Post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('User', backref='posts')

    # Use 'through' relationship to conenct posts directly to tags through posts_tags table
    tags = db.relationship('Tag', secondary="posts_tags", backref="posts", cascade="all, delete")

    # post_tag = db.relationship('PostTag', backref="posts")

    def __repr__(self):
        return f"<Post {self.title} {self.created_at} {self.user_id} >"

class PostTag(db.Model):
    """Post and Tag relationship model"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

    # post_tag = db.relationship('PostTag', backref="tags")

    # # Use 'through' relationship to conenct posts directly to tags through posts_tags table
    # # ASK TA/MENTOR: Can't get this to delete posts-tags relationships
    # posts = db.relationship('Tag', secondary="posts_tags", backref="tags", cascade="all, delete")

