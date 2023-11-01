import pytest
import json
from app import app, db, User, Content, Category

# Initialize the Flask app and set the testing environment
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a test database

@pytest.fixture
def client():
    # Create a test client using the Flask app context
    with app.test_client() as client:
        # Create the test database
        db.create_all()
        yield client

    # After the test, clean up the database
    db.drop_all()

def test_get_data(client):
    response = client.get('/')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Welcome to Moringa Daily'

def test_content_routes(client):
    # Create a sample user
    user = User(username='testuser', email='test@example.com', role='user')
    db.session.add(user)
    db.session.commit()

    # Create a sample category
    category = Category(name='Test Category', description='Test Description')
    db.session.add(category)
    db.session.commit()

    # Test adding content
    content_data = {
        'title': 'Test Article',
        'description': 'This is a test article.',
        'category_id': category.category_id,
        'user_id': user.id,
        'content_type': 'article',
        'rating': 5,
        'is_flagged': False,
        'image_thumbnail': 'test_image.jpg',
        'video_url': 'test_video.mp4',
        'status': 'published'
    }
    response = client.post('/api/content', json=content_data)
    data = json.loads(response.data)
    assert response.status_code == 201
    assert data['title'] == 'Test Article'

    # Test retrieving content
    response = client.get('/api/content')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['title'] == 'Test Article'

def test_user_list(client):
    response = client.get('/users')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 0  # No users initially

    # Create a sample user
    user = User(username='testuser', email='test@example.com', role='user')
    db.session.add(user)
    db.session.commit()

    response = client.get('/users')
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['username'] == 'testuser'

def test_create_category(client):
    category_data = {
        'name': 'Test Category',
        'description': 'Test Description'
    }
    response = client.post('/admin/create-category', json=category_data)
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['message'] == 'Category created successfully'

def test_view_categories(client):
    # Create a sample category
    category = Category(name='Test Category', description='Test Description')
    db.session.add(category)
    db.session.commit()

    response = client.get('/view-categories')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['name'] == 'Test Category'

def test_add_to_wishlist(client):
    # Create a sample user
    user = User(username='testuser', email='test@example.com', role='user')
    db.session.add(user)
    db.session.commit()

    # Create a sample content
    content_data = {
        'title': 'Test Article',
        'description': 'This is a test article.',
        'category_id': 1,
        'user_id': 1,
        'content_type': 'article',
        'rating': 5,
        'is_flagged': False,
        'image_thumbnail': 'test_image.jpg',
        'video_url': 'test_video.mp4',
        'status': 'published'
    }
    db.session.add(Content(**content_data))
    db.session.commit()

    # Add the article to the user's wishlist
    wishlist_data = {
        'user_id': 1
    }
    response = client.post('/add-to-wishlist/1', json=wishlist_data)
    assert response.status_code == 200

    # Check if the article is in the user's wishlist
    user = User.query.get(1)
    assert user.wishlists[0].title == 'Test Article'

def test_remove_from_wishlist(client):
    # Create a sample user
    user = User(username='testuser', email='test@example.com', role='user')
    db.session.add(user)
    db.session.commit()

    # Create a sample content
    content_data = {
        'title': 'Test Article',
        'description': 'This is a test article.',
        'category_id': 1,
        'user_id': 1,
        'content_type': 'article',
        'rating': 5,
        'is_flagged': False,
        'image_thumbnail': 'test_image.jpg',
        'video_url': 'test_video.mp4',
        'status': 'published'
    }
    db.session.add(Content(**content_data))
    db.session.commit()

    # Add the article to the user's wishlist
    wishlist_data = {
        'user_id': 1
    }
    response = client.post('/add-to-wishlist/1', json=wishlist_data)
    assert response.status_code == 200

    # Remove the article from the user's wishlist
    response = client.post('/remove-from-wishlist/1', json=wishlist_data)
    assert response.status_code == 200

    # Check if the user's wishlist is empty
    user = User.query.get(1)
    assert len(user.wishlists) == 0

# Run the tests
if __name__ == '__main__':
    pytest.main()
