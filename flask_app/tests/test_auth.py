import unittest
from app import create_app, db
from app.users.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_register_page_loads(self):
        response = self.client.get('/users/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)
    
    def test_login_page_loads(self):
        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_user_registration(self):
        response = self.client.post('/users/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        user = db.session.execute(
            db.select(User).where(User.username == 'testuser')
        ).scalar_one_or_none()
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
    
    def test_user_login_logout(self):
        user = User(
            username='testuser',
            email='test@example.com',
            password=User().hash_password('password123')
        )
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/users/login', data={
            'email': 'test@example.com',
            'password': 'password123',
            'remember': False
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)
        
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
