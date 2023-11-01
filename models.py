from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True,)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(50))
    
    contents = db.relationship('Content', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)
    wishlists = db.relationship('Wishlist', backref='user', lazy=True)

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    contents = db.relationship('Content', backref='category', lazy=True)
    subscriptions = db.relationship('Subscription', backref='category', lazy=True)

class Content(db.Model):
    content_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_type = db.Column(db.String(50))
    is_published = db.Column(db.String)
    is_flagged = db.Column(db.String)
    
    comments = db.relationship('Comment', backref='content', lazy=True)
    wishlists = db.relationship('Wishlist', backref='content', lazy=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Subscription(db.Model):
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

class Wishlist(db.Model):
    wishlist_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id'))
