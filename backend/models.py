from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # 최대 50자의 문자열
    email = Column(String(100), unique=True, index=True)  # 최대 100자의 문자열
    hashed_password = Column(String(255))

    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # 최대 255자의 문자열
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))  # Post 모델 참조를 위한 외래 키

    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')
