from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import the datetime module
from sqlalchemy_serializer import SerializerMixin
db = SQLAlchemy()


# Define the User model
class User(db.Model, SerializerMixin):

    serialize_only = ("id", "username", "email", "password", "role")

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(50))  # User's role (Admin, Reader, Writer)

    # Constructor for User model
    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

# Define the Category model
class Category(db.Model, SerializerMixin):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

# Define the Content model
class Content(db.Model, SerializerMixin):
    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_type = db.Column(db.String(50))
    rating = db.Column(db.String)
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)  # Set the default to the current time
    is_flagged = db.Column(db.String)
    image_thumbnail = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    status = db.Column(db.String)


    # Define relationships between Content, Category, and User models
    category = db.relationship('Category', backref='contents')
    user = db.relationship('User', backref='contents')

# Define the Comment model
class Comment(db.Model, SerializerMixin):
    comment_id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)

    # Define relationships between Comment, Content, and User models
    content = db.relationship('Content', backref='comments')
    user = db.relationship('User', backref='comments')

# Define the Subscription model
class Subscription(db.Model, SerializerMixin):
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    # Define relationships between Subscription, User, and Category models
    user = db.relationship('User', backref='subscriptions')
    category = db.relationship('Category', backref='subscribers')

# Define the Wishlist model
class Wishlist(db.Model, SerializerMixin):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))

    # Define relationships between Wishlist, User, and Content models
    user = db.relationship('User', backref='wishlists')
    content = db.relationship('Content', backref='wished_by')
