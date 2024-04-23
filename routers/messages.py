from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.database import get_db
from auth.models import CreateMessageRequest, Users
from auth.token import get_current_user


messages_router = APIRouter(prefix="/message", tags=["Messages"])


@messages_router.post("/")
def create_message(
    message: CreateMessageRequest,
    current_user: Users = Depends(get_current_user),
    #user_receiver_id: Users = Depends(get_user),    #must create get_user to verify the existance of user (receiver)
    db: Session = Depends(get_db)
):  
    return create_message(db, message, current_user)


@messages_router.get("/conversations")
def view_conversations():
    pass


@messages_router.get("/conversation/{user_id}")
def view_conversation(user_id: int):
    pass