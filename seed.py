from models import User,Category,Content,Wishlist,Subscription,Comment,db
from app import app
from werkzeug.security import generate_password_hash,check_password_hash
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255))
#     email = db.Column(db.String(255))
#     password = db.Column(db.String(255))
#     role = db.Column(db.String(50))  # User's role (Admin, Reader, Writer)
with app.app_context ():
    User.query.delete()

    user1 = User(username="admin", email="admin@example.com", password="hashed_password", role="admin")
    user2 = User(username="techwriter", email="writer@example.com", password="hashed_password", role="techwriter")
    user3 = User(username="user", email="user@example.com", password="hashed_password", role="user")

    db.session.add_all([user1, user2, user3])
    db.session.commit()


    category1 = Category(name="DevOps", description="DevOps-related content")
    category2 = Category(name="Fullstack", description="Fullstack development content")
    category3 = Category(name="Front-End", description="Front-End development content")

    db.session.add_all([category1, category2, category3])
    db.session.commit()


    # Retrieve the users for associating with content
    admin_user = User.query.filter_by(username="admin").first()
    techwriter_user = User.query.filter_by(username="techwriter").first()
    user_user = User.query.filter_by(username="user").first()

    content1 = Content(
        title="Tech Interview Tips",
        description="How to prepare for technical interviews",
        category_id=2,  # Assuming Fullstack category
        user_id=techwriter_user.id,
        content_type="video",
        rating="5",
        is_flagged=False,
        image_thumbnail="thumbnail_url",
        video_url="video_url",
        status="approved"
    )

    content2 = Content(
        title="DevOps Best Practices",
        description="Key practices for DevOps professionals",
        category_id=1,  # Assuming DevOps category
        user_id=techwriter_user.id,
        content_type="article",
        rating="4",
        is_flagged=False,
        image_thumbnail="thumbnail_url",
        video_url=None,
        status="approved"
    )

    content3 = Content(
        title="Web Development Trends",
        description="The latest trends in front-end development",
        category_id=3,  # Assuming Front-End category
        user_id=techwriter_user.id,
        content_type="article",
        rating="4",
        is_flagged=False,
        image_thumbnail="thumbnail_url",
        video_url=None,
        status="approved"
    )

    db.session.add_all([content1, content2, content3])
    db.session.commit()

def create_default_comments():
    # Retrieve the content and users for associating with comments
    content1 = Content.query.filter_by(title="Tech Interview Tips").first()
    content2 = Content.query.filter_by(title="DevOps Best Practices").first()
    content3 = Content.query.filter_by(title="Web Development Trends").first()
    
    techwriter_user = User.query.filter_by(username="techwriter").first()
    user_user = User.query.filter_by(username="user").first()
    
    comment1 = Comment(
        content_id=content1.content_id,
        user_id=techwriter_user.id,
        text="Great video, very informative!"
    )

    comment2 = Comment(
        content_id=content1.content_id,
        user_id=user_user.id,
        text="I found this video really helpful for my interview preparation."
    )

    comment3 = Comment(
        content_id=content2.content_id,
        user_id=techwriter_user.id,
        text="DevOps is a fascinating field, and these practices are essential."
    )

    db.session.add_all([comment1, comment2, comment3])
    db.session.commit()

