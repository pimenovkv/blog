from blog_app import db
from sqlalchemy import Column, Integer, String


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    email = Column(String(128), unique=True)
    password_hash = Column(String(128), unique=True)

    def __repr__(self):
        return f'<User {self.name}>'
