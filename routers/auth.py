from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.database import get_db
from auth.models import User, CreateUserRequest, Token
from auth.roles import Roles
from auth.security import get_password_hash, verify_password
from auth.token import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRATION_MINS


auth_router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


def verify_username(db: Session, username: str):
    """
    Checks if the username already exists in the database.
    """
    user = db.query(User).filter(User.username == username).first()
    return user is not None


def authenticate_user(username: str, password: str, db):
    """
    Searches through the database and tries to find a match
    for the username which is being passed for the same user
    in the database
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect username.")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Incorrect password.")
    return user


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    if verify_username(db, create_user_request.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Username already exists.")
    create_user_model = User(username=create_user_request.username,
                              hashed_password=get_password_hash(create_user_request.password))
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"id": create_user_model.id, "username": create_user_model.username}


@auth_router.get("/user_info", status_code=status.HTTP_200_OK)
async def user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Authentication has failed.")
    return {"user": user}


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS))
    return {"access_token": token, "token_type": "bearer"}


def ensure_admin_user(user: User = Depends(get_current_user)):
    if user.role != Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can perform this action.")
    return user


@auth_router.put("/users/{user_id}/role", status_code=status.HTTP_200_OK, dependencies=[Depends(ensure_admin_user)])
async def update_user_role(user_id: int, new_role: Roles, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} not found.")
    
    user.role = new_role
    db.commit()
    
    return {"message": f"User role updated to {new_role.value}"}