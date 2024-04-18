from fastapi import FastAPI, Depends, HTTPException, status
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import Annotated


app = FastAPI()

models = models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: None, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    return {"user": user}