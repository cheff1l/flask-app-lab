from datetime import datetime
from app import db


class Post(db.Model):
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    category = db.Column(db.Enum('news', 'publication', 'tech', 'other', name='category_types'))
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default='Anonymous')
    
    def __repr__(self):
        return f'<Post {self.title}>'
