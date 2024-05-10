from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database import get_db
from data.models import CreateMessageRequest, Message, User
from auth.token import get_current_user
from services.message_service import create_message, get_conversations, get_conversation


message_router = APIRouter(prefix="/messages", tags=["messages"])


@message_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_message(message: CreateMessageRequest,
                       current_user: User = Depends(get_current_user), 
                       db: Session = Depends(get_db)):  
    return create_message(message, current_user, db)


@message_router.get("/conversations")
def view_conversations(current_user: User = Depends(get_current_user), 
                       db: Session = Depends(get_db)):  
    return get_conversations(db, current_user.id)


@message_router.get("/conversation/{user_id}")
def view_conversation(user_id: int, 
                      current_user: User = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    return get_conversation(db, current_user.id, user_id)