from models import User, Category, Content, Comment, db
from app import app
from werkzeug.security import generate_password_hash

def create_default_data():
    with app.app_context():
        # Clear existing data (if needed)
        db.drop_all()
        db.create_all()

        # Create default users
        user1 = User(username="admin", email="admin@example.com", password=generate_password_hash("admin_password"), role="admin")
        user2 = User(username="techwriter", email="techwriter@example.com", password=generate_password_hash("techwriter_password"), role="techwriter")
        user3 = User(username="user", email="user@example.com", password=generate_password_hash("user_password"), role="user")

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        # Create default categories
        category1 = Category(name="DevOps")
        category2 = Category(name="Fullstack")
        category3 = Category(name="Front-End")

        db.session.add_all([category1, category2, category3])
        db.session.commit()

        # Create default content
        content1 = Content(
            title="Tech Interview Tips",
            description="How to prepare for technical interviews",
            category_id=2,  # Assuming Fullstack category
            user_id=user2.id,
            is_flagged=False,
            media_url="https://plus.unsplash.com/premium_photo-1684769160411-ab16f414d1bc?q=80&w=1163&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        )

        content2 = Content(
            title="Healthy Recipes",
            description="Delicious and nutritious recipes for a healthy lifestyle",
            category_id=3,  # Assuming Recipes category
            user_id=user3.id,
            is_flagged=False,
            media_url="video_url2"
        )

        content3 = Content(
            title="Travel Adventures",
            description="Explore the world's most exciting travel destinations",
            category_id=4,  # Assuming Travel category
            user_id=user1.id,
            is_flagged=False,
            media_url="video_url3"
        )

        content4 = Content(
            title="Book Reviews",
            description="Reviews of the latest bestsellers and hidden gems",
            category_id=5,  # Assuming Books category
            user_id=user2.id,
            is_flagged=False,
            media_url="video_url4"
        )

        content5 = Content(
            title="Fitness Workouts",
            description="Effective workouts to stay fit and healthy",
            category_id=6,  # Assuming Fitness category
            user_id=user3.id,
            is_flagged=False,
            media_url="video_url5"
        )

        db.session.add_all([content1, content2, content3, content4, content5])
        db.session.commit()

        # Create default comments
        comment1 = Comment(
            content_id=content1.content_id,
            user_id=user2.id,
            text="Great video, very informative!"
        )

        comment2 = Comment(
            content_id=content1.content_id,
            user_id=user3.id,
            text="I found this video really helpful for my interview preparation."
        )

        comment3 = Comment(
            content_id=content2.content_id,
            user_id=user2.id,
            text="DevOps is a fascinating field, and these practices are essential."
        )

        db.session.add_all([comment1, comment2, comment3])
        db.session.commit()

if __name__ == '__main__':
    create_default_data()
