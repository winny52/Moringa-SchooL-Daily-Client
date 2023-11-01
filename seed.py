# from app import app, db
# from app.models import User, Category, Content, Comment, Subscription, Wishlist

# def create_users():
#     # Create and insert user data into the database
#     user1 = User(username="Denzel Washington", email="denzel@example.com", password="password1", role="Admin")
#     user2 = User(username="Lupita Nyong'o", email="lupita@example.com", password="password2", role="Tech Writer")
#     user3 = User(username="Silvester Stalone", email="silvester@example.com", password="password3", role="Reader")

#     # Add users to the database session
#     db.session.add(user1)
#     db.session.add(user2)
#     db.session.add(user3)

# if __name__ == "__main__":
#     with app.app_context():
#         create_users()
