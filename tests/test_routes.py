import unittest
import json
from app import app, db, User, Content, Comment, Category
import pytest

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_list_route(self):
        with app.app_context():
            # Create a test user
            user = User(username='test_user', email='test@example.com', role='user', password='password')
            db.session.add(user)
            db.session.commit()

            response = self.app.get('/users')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['username'], 'test_user')

    def test_create_category_route(self):
        with app.app_context():
            data = {
                'name': 'Test Category',
                'description': 'Test Description'
            }
            response = self.app.post('/admin/create-category', json=data)
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Category created successfully')

    def test_view_categories_route(self):
        with app.app_context():
            # Create test categories
            category1 = Category(name='Category 1', description='Description 1')
            category2 = Category(name='Category 2', description='Description 2')
            db.session.add_all([category1, category2])
            db.session.commit()

            response = self.app.get('/view-categories')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], 'Category 1')

    def test_content_route(self):
        with app.app_context():
            data = {
                'title': 'Test Content',
                'description': 'Test Description',
                'category_id': 1,
                'user_id': 1,
                'content_type': 'article',
                'rating': 5,
                'is_flagged': False,
                'image_thumbnail': 'thumbnail.jpg',
                'video_url': 'video.mp4',
                'status': 'published'
            }

            response = self.app.post('/api/content', json=data)
            self.assertEqual(response.status_code, 201)
            response = self.app.get('/api/content')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['title'], 'Test Content')

    def test_update_content_route(self):
        with app.app_context():
            # Create test content
            content = Content(
                title='Test Content',
                description='Test Description',
                category_id=1,
                user_id=1,
                content_type='article',
                rating=5,
                is_flagged=False,
                image_thumbnail='thumbnail.jpg',
                video_url='video.mp4',
                status='published'
            )
            db.session.add(content)
            db.session.commit()

            data = {
                'title': 'Updated Title',
                'description': 'Updated Description',
                'content_type': 'updated',
                'rating': 4,
                'is_flagged': True,
                'image_thumbnail': 'updated.jpg',
                'video_url': 'updated.mp4',
                'status': 'draft'
            }

            response = self.app.put(f'/content/{content.content_id}', json=data)
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Content updated successfully')
            self.assertEqual(data['content']['title'], 'Updated Title')
            self.assertEqual(data['content']['description'], 'Updated Description')

    def test_delete_content_route(self):
        with app.app_context():
            # Create test content
            content = Content(
                title='Test Content',
                description='Test Description',
                category_id=1,
                user_id=1,
                content_type='article',
                rating=5,
                is_flagged=False,
                image_thumbnail='thumbnail.jpg',
                video_url='video.mp4',
                status='published'
            )
            db.session.add(content)
            db.session.commit()

            response = self.app.delete(f'/content/{content.content_id}')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Content deleted successfully')

    def test_get_or_create_comments_route(self):
        with app.app_context():
            # Create test content
            content = Content(
                title='Test Content',
                description='Test Description',
                category_id=1,
                user_id=1,
                content_type='article',
                rating=5,
                is_flagged=False,
                image_thumbnail='thumbnail.jpg',
                video_url='video.mp4',
                status='published'
            )
            db.session.add(content)
            db.session.commit()

            response = self.app.get(f'/content/{content.content_id}/comments')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 0)

            comment_data = {
                'user_id': 1,
                'text': 'Test Comment'
            }
            response = self.app.post(f'/content/{content.content_id}/comments', json=comment_data)
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Comment added successfully')

    def test_delete_comment_route(self):
        with app.app_context():
            # Create test comment
            comment = Comment(
                content_id=1,
                user_id=1,
                text='Test Comment'
            )
            db.session.add(comment)
            db.session.commit()

            response = self.app.delete(f'/comments/{comment.comment_id}')
            data = json.loads(response.data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['message'], 'Comment deleted successfully')

    def test_add_to_wishlist_route(self):
        with app.app_context():
            # Create a test user
            user = User(username='test_user', email='test@example.com', role='user', password='password')
            db.session.add(user)

            # Create a test content
            content = Content(
                title='Test Content',
                description='Test Description',
                category_id=1,
                user_id=1,
                content_type='article',
                rating=5,
                is_flagged=False,
                image_thumbnail='thumbnail.jpg',
                video_url='video.mp4',
                status='published'
            )
            db.session.add(content)

            db.session.commit()

            # data = {
            #     'user_id': user.id,
            #     'content_id': content.id
            # }
            # response = self.app.post('/wishlist', json=data)
            # data = json.loads(response.data)
            # self.assertEqual(response.status_code, 200)
            # self.assertEqual(data['message'], 'Content added to wishlist successfully')
           

    def test_remove_from_wishlist_route(self):
        with app.app_context():
            # Create a test user
            user = User(username='test_user', email='test@example.com', role='user', password='password')
            db.session.add(user)
    
    def test_user_registration_route(self):
        with app.app_context():
            data = {
                'username': 'new_user',
                'email': 'new@example.com',
                'password': 'new_password'
            }
            

    def test_user_login_route(self):
        with app.app_context():
            # Create a test user
            user = User(username='test_user', email='test@example.com', role='user', password='password')
            db.session.add(user)
            db.session.commit()

            data = {
                'email': 'test@example.com',
                'password': 'password'
            }
            

    def test_user_specific_functionality_route(self):
        with app.app_context():
            # Create a test user
            user = User(username='test_user', email='test@example.com', role='user', password='password')
            db.session.add(user)
            db.session.commit()

            # Simulate user-specific functionality
            data = {
                'user_id': user.id,
                'param1': 'value1',
                'param2': 'value2'
            }
            

    def test_error_handling_route(self):
        with app.app_context():
            # Simulate an error scenario
            data = {
                'invalid_field': 'value'
            }
            


if __name__ == '__main__':
    unittest.main()
