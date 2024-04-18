from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from jwt.database import SessionLocal
from jwt.models import CreateUserRequest, Users, Token
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "4f1feeca525de4cdb064656007da3edac7895a87ff0ea865693300fb8b6e8f9c"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(name=create_user_request.name,
                              hashed_password=bcrypt.hash(create_user_request.password))
    db.add(create_user_model)
    db.commit()
