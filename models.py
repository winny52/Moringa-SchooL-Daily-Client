from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

# Define the User model
class User(db.Model):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(255))
     email = db.Column(db.String(255))
     password = db.Column(db.String(255))
     role = db.Column(db.String(50))

    #  def __init__(self, username, email, password, role):
    #     self.username = username
    #     self.email = email
    #     self.password = password
    #     self.role = role
     def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role  # Add other fields as needed
        }
# Define the Category model
class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    # Define relationships between Category and Content models
    contents = db.relationship('Content', backref='category', lazy=True)

# Define the Content model
class Content(db.Model):
    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_flagged = db.Column(db.Boolean, default=False)
    media_url = db.Column(db.String(255))
    average_rating = db.Column(db.Float)
    # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # created_at = db.Column(datetime)

    # Define relationships between Content, User, and Rating models
    user = db.relationship('User', backref='contents', lazy=True)
    ratings = db.relationship('Rating', backref='content', lazy=True)

    # Add a method to calculate the average rating
    def calculate_average_rating(self):
        total_ratings = sum(rating.rating for rating in self.ratings)
        num_ratings = len(self.ratings)
        if num_ratings > 0:
            self.average_rating = total_ratings / num_ratings
        else:
            self.average_rating = 0.0

# Define the Comment model
class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column(db.Text)

    # Define relationships between Comment, Content, and User models
    content = db.relationship('Content', backref='comments', foreign_keys=[content_id])
    user = db.relationship('User', backref='user_comments', foreign_keys=[user_id])

# Define the Subscription model
class Subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    # Define relationships between Subscription, User, and Category models
    user = db.relationship('User', backref='subscriptions', lazy=True)
    category = db.relationship('Category', backref='subscribers', lazy=True)

# Define the Wishlist model
class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))

    # Define relationships between Wishlist, User, and Content models
    user = db.relationship('User', backref='wishlists', lazy=True)
    content = db.relationship('Content', backref='wished_by', lazy=True)

# Ratings model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)

    # Define relationships between Rating, Content, and User models
    user = db.relationship('User', backref='ratings', lazy=True)
