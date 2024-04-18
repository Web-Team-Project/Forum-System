from jwt.database import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    hashed_password = Column(String)

class CreateUserRequest(BaseModel):
    name: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str