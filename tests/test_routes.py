# test_app.py
import json
import pytest
from app import app

class TestApp:
    '''Moringa Daily Api Tests'''

    def test_index_route(self):
        '''Test the root route'''
        response = app.test_client().get('/')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert data == {'message': 'Welcome to Moringa Daily'}

    def test_get_user_data_route(self):
        '''Test the route to get user data'''
        response = app.test_client().get('/user_data')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'username' in data
        assert 'email' in data

    def test_post_user_data_route(self):
        '''Test the route to post user data'''
        user_data = {'username': 'test_user', 'email': 'test@example.com'}
        response = app.test_client().post('/user_data', json=user_data)
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'message' in data

    def test_get_category_data_route(self):
        '''Test the route to get category data'''
        response = app.test_client().get('/category_data')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'name' in data
        assert 'description' in data

    def test_post_category_data_route(self):
        '''Test the route to post category data'''
        category_data = {'name': 'TestCategory', 'description': 'A test category'}
        response = app.test_client().post('/category_data', json=category_data)
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert 'message' in data

   
    def test_authenticated_route(self):
        '''Test an authenticated route'''
        # Make a request with authentication, and check the response
        # Add assertions for the expected response data

    
    def test_unauthenticated_route(self):
        '''Test an unauthenticated route'''
        

if __name__ == '__main__':
    pytest.main()
