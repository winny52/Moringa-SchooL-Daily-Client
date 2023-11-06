import json
from app import app, db, User, Content, Comment, Category
import pytest
class TestApp:
    '''Moringa Daily Api Tests'''
    def test_get_data_route(self):
       response = app.test_client().get('/')
       assert response.status_code == 200
       data = json.loads(response.data.decode('utf-8'))
       assert data ==  {'message' : 'Welcome to Moringa Daily'}
       assert type (data)==dict

    def test_get_user_data_route(self):
        response = app.test_client().get('/users')
        assert response.status_code == 200
        data = json.loads(response.data.decode('utf-8'))
        assert type (data)==list
        assert 'email' in data[0]  

    def test_get_category_route(self):
        response = app.test_client().get('/view-categories')    

    def test_get_content_route(self):
        response = app.test_client().get('/api/content')
        assert response.status_code == 200
        content_data = json.loads(response.data.decode('utf-8'))
        assert type(content_data) == list
        assert 'title' in content_data[0]


    






