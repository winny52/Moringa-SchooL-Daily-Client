# tests/test_routes.py
import json
import pytest
from your_flask_app import create_app
from your_flask_app.models import db, User, Content

@pytest.fixture
def app():
    app = create_app(test_config=True)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)


def test_get_user(client):
    user_id = 1  # Adjust to an existing user ID in your test database
    response = client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, dict)
    # Add assertions for user data

def test_get_content(client):
    response = client.get('/api/content')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    

def test_login(client):
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/api/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'access_token' in data


