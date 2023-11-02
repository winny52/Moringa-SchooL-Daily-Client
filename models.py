from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# Define the User model
class User(db.Model):

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
class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))

# Define the Content model
class Content(db.Model):
    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    is_flagged = db.Column(db.Integer)
    media_url = db.Column(db.String(255)) 

    average_rating = db.Column(db.Float)

# Define relationships between Content, Category, and User models
    category = db.relationship('Category', backref='contents')
    ratings = db.relationship('Rating', backref='rated_content')


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
    content = db.relationship('Content', backref='comments', foreign_keys=[content_id])  # Define the foreign_keys parameter to specify the relationship.
    user = db.relationship('User', backref='user_comments', foreign_keys=[user_id])  # Define the foreign_keys parameter to specify the relationship.


# Define the Subscription model
class Subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    # Define relationships between Subscription, User, and Category models
    user = db.relationship('User', backref='subscriptions')
    category = db.relationship('Category', backref='subscribers')

# Define the Wishlist model
class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))

    # Define relationships between Wishlist, User, and Content models
    user = db.relationship('User', backref='wishlists')
    content = db.relationship('Content', backref='wished_by')

#Ratings model
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)

    # Define relationships between Rating, Content, and User models
    content = db.relationship('Content', backref='content_ratings')
    user = db.relationship('User', backref='ratings')

