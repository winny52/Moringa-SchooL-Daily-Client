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
      assert type(data)==dict


   def test_get_user_data_route(self):
      '''Test the route to get user data'''
      response = app.test_client().get('/users')
      assert response.status_code == 200
      data = json.loads(response.data.decode('utf-8'))
   
      assert type(data)==list
      assert 'email' in data[0]
   
   def test_get_category_route (self):
      '''Test tI am hoping we can find an alternative date and time that works for both of us to ensure that we can have a productive and meaningful discussion. Please let me know your availability, and I will do my best to accommodate your schedule.

he route to get category'''
      response =app.test_client().get('/view-categories')
      assert response.status_code== 200
      data.json.loads(response.data.decode)