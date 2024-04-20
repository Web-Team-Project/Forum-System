from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from auth.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)


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
    #category = Column(String, index=True)
    author = Column(Integer, ForeignKey("users.id"))


class CreateTopicRequest(BaseModel):
    title: str
    #category: str