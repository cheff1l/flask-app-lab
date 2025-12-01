import unittest
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    
    def setUp(self):
        """Налаштування тестового середовища"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        
        # Створення бази в контексті додатка
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Очищення бази після кожного тесту"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_post(self):
        """US01: Створити новий пост"""
        with self.app.app_context():
            response = self.client.post("/post/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "is_active": True,
                "publish_date": "2024-11-19T10:00",
                "category": "tech"
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)
            
            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")
    
    def test_list_posts(self):
        """US02: Перегляд усіх постів"""
        with self.app.app_context():
            # Додаємо тестовий пост
            post = Post(title="Test", content="Content", category="tech")
            db.session.add(post)
            db.session.commit()
            
            response = self.client.get("/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Test", response.data)
    
    def test_view_post_detail(self):
        """US03: Перегляд одного поста"""
        with self.app.app_context():
            post = Post(title="Detail Test", content="Test Content", category="tech")
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            
            response = self.client.get(f"/post/{post_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detail Test", response.data)
    
    def test_update_post(self):
        """US04: Редагування поста"""
        with self.app.app_context():
            post = Post(title="Old Title", content="Old Content", category="tech")
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            
            response = self.client.post(f"/post/{post_id}/update", data={
                "title": "New Title",
                "content": "New Content",
                "is_active": True,
                "publish_date": "2024-11-19T10:00",
                "category": "news"
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            
            updated_post = db.session.get(Post, post_id)
            self.assertEqual(updated_post.title, "New Title")
    
    def test_delete_post(self):
        """US05: Видалення поста"""
        with self.app.app_context():
            post = Post(title="To Delete", content="Content", category="tech")
            db.session.add(post)
            db.session.commit()
            post_id = post.id
            
            response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            
            deleted_post = db.session.get(Post, post_id)
            self.assertIsNone(deleted_post)
    
    def test_404_not_found(self):
        """US06: 404 при відсутньому пості"""
        with self.app.app_context():
            response = self.client.get("/post/9999")
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
