from blog_app import db, login
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class Users(UserMixin, db.Model):
    """
    Класс, описывающий модель данных пользователя.
    Наследуется от UserMixin для работы с Flask-Login.
    """
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(128), unique=True)
    password_hash = Column(String(128), unique=True)
    posts = relationship('Posts', backref='author', lazy='dynamic')
    comments = relationship('Comments', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Posts(db.Model):
    """
    Класс, описывающий модель данных поста пользователя.
    """
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
    """
    Класс, описывающий модель данных комментария от пользователя к посту пользователя.
    """
    id = Column(Integer, primary_key=True)
    body = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))

    def __repr__(self):
        return f'<Comment {self.body}>'


# Колбэк для чтения данных о пользователе из БД
@login.user_loader
def load_user(id):
    return Users.query.get(int(id))
