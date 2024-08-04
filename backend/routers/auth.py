from datetime import timedelta
from typing import Annotated

from auth.security import get_password_hash, verify_password
from auth.token import (
    ACCESS_TOKEN_EXPIRATION_MINS,
    create_access_token,
    get_current_user,
)
from data.database import get_db
from data.models import User
from data.schemas import CreateUserRequest, Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.user_service import verify_username
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def authenticate_user(username: str, password: str, db):
    """
    Searches through the database and tries to find a match
    for the username which is being passed for the same user
    in the database
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username."
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
        )
    return user


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    if verify_username(db, create_user_request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists."
        )
    create_user_model = User(
        username=create_user_request.username,
        hashed_password=get_password_hash(create_user_request.password),
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"id": create_user_model.id, "username": create_user_model.username}


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    token = create_access_token(
        user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS)
    )
    return {"access_token": token, "token_type": "bearer"}
