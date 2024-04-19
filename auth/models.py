from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from auth.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


# class Category(Base):
#     __tablename__ = 'categories'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     description = Column(String)
#     topics = relationship("Topic", back_populates="category")
#
#
# class Topic(Base):
#     __tablename__ = "topics"
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     category_id = Column(Integer, ForeignKey('categories.id'))
#     created_at = Column(DateTime, default=datetime.utcnow)
#     user = relationship("User", back_populates="topics")
#     category = relationship("Category", back_populates="topics")