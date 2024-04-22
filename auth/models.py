from enum import Enum
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from auth.database import Base


class Roles(Enum):
    user = "user"
    admin = "admin"


class Users(Base): # Rename to User and move router and services to user
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Roles), default="user")


class CreateUserRequest(BaseModel):
    username: str
    password: str


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
    category_id: str


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)


class CreateCategoryRequest(BaseModel):
    name: str