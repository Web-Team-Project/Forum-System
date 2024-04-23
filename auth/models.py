from enum import Enum
from pydantic import BaseModel, conint, validator
from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, Text
from sqlalchemy.sql import func
from auth.database import Base
from auth.roles import Roles
from sqlalchemy.orm import relationship


class Users(Base): # Rename to User and move router and services to user
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Roles), default="user")

    votes = relationship("Vote", back_populates="user")


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


class Message(Base):
    __tablename__ = "Message"
    id = Column(Integer, primary_key=True, index=True)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    user_sender_id = Column(Integer, index=True)   #must be user
    user_reciever_id = Column(Integer, index=True) #must be user
    text = Column(String, index=True)


class CreateMessageRequest(BaseModel):
    text:str


class Reply(Base):
    __tablename__ = "replies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    #Foreign Keys
    user_id = Column(Integer, ForeignKey('users.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))

    votes = relationship("Vote", back_populates="reply")


class CreateReplyRequest(BaseModel):
    content: str
    topic_id: int


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    reply_id = Column(Integer, ForeignKey("replies.id"), primary_key=True)
    vote_type = Column(Integer)

    user = relationship("Users", back_populates="votes")
    reply = relationship("Reply", back_populates="votes")


class CreateVote(BaseModel):
    vote_type: conint(ge=-1, le=1)

    @validator('vote_type')
    def check_vote_type(cls, v):
        if v not in(-1, 1):
            raise ValueError('vote_type must be either -1 (downvote) or 1 (upvote)')
        return v
