from database import Base, BaseModel
from sqlalchemy import Column, Integer, String


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