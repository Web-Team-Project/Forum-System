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
from jose import jwt, JWTError


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

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
        user = authenticate_user(form_data.name, form_data.password)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                 detail="Incorrect username or password.")
        token = create_access_token(user.name, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
                                    
        return {"access_token": token, "token_type": "bearer"}

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)

# Searches through SQLite database and tries to find a match
# for the username which is being passed for the same username
# in the database
def authenticate_user(name: str, password: str, db):
    user = db.query(Users).filter(Users.name == name).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username.")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password.")
    return user

def create_access_token(name: str, user_id: int, expires_in: timedelta):
    encode = {"sub": name, "id": user_id}
    expiration = datetime.now() + expires_in
    encode.update({"exp": expiration})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)