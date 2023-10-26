import json
import pytest
from app import app # Import your Flask app

class TestApp:
     '''Moringa Daily Api  '''
     def test_get_data_route(self):
        '''has a resource at "/"'''
        response = app.test_client().get('/')
        assert response.status_code == 200  
        data = json.loads(response.data.decode('utf-8'))  
        assert data == {'message': 'Welcome to Moringa Daily'}

     