from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth.database import SessionLocal
from auth.models import CreateUserRequest, Users, Token
from auth.security import password_context, verify_password
from auth.token import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRATION_MINS


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
oath2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Searches through SQLite database and tries to find a match
# for the userusername which is being passed for the same userusername
# in the database
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username.")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    return user


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(username=create_user_request.username,
                              hashed_password=password_context.hash(create_user_request.password))
    db.add(create_user_model)
    db.commit()


@auth_router.get("/user_info", status_code=status.HTTP_200_OK)
async def user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    return {"user": user}


@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Incorrect username or password.")
        token = create_access_token(user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINS))
                                    
        return {"access_token": token, "token_type": "bearer"}