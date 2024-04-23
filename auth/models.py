from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text
from sqlalchemy.sql import func
from auth.database import Base
from auth.roles import Roles


class Users(Base): # Rename to User and move router and services to user
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Roles), default="user")


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: Roles


class Token(BaseModel):
    access_token: str
    token_type: str


class Topics(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    author_id = Column(Integer, ForeignKey("users.id"))


class CreateTopicRequest(BaseModel):
    title: str
    category_id: int


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class CreateCategoryRequest(BaseModel):
    name: str


class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    up_votes = Column(Integer, default=0)
    down_votes = Column(Integer, default=0)

    #Foreign Keys
    user_id = Column(Integer, ForeignKey('users.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))


class CreateReplyRequest(BaseModel):
    content: str
    topic_id: int


