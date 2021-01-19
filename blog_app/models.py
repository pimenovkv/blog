from blog_app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(128), unique=True)
    posts = relationship('Posts', backref='author', lazy='dynamic')
    comments = relationship('Comments', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'


class Posts(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    like_num = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'))
    comments = relationship('Comments', backref='post', lazy='dynamic')

    def __repr__(self):
        return f'<Post {self.title}>'


class Comments(db.Model):
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment {self.body}>'
