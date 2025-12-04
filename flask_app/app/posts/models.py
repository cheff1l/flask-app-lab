from datetime import datetime
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    category = db.Column(db.Enum('news', 'publication', 'tech', 'other', name='category_types'))
    is_active = db.Column(db.Boolean, default=True)
    
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    
    tags: Mapped[List["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f'<Post {self.title}>'


class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)
    
    posts: Mapped[List["Post"]] = relationship(secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f'<Tag {self.name}>'