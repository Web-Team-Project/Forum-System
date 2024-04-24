from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from auth.database import get_db
from auth.models import CreateMessageRequest, Message, Users
from auth.token import get_current_user
from services import message_service

message_router = APIRouter(prefix="/message", tags=["Messages"])


@message_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_message(
    message: CreateMessageRequest,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    # Find the receiver in the database
    receiver = db.query(Users).filter(Users.id == message.receiver_id).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    # Create the message
    db_message = Message(
        text=message.text,
        sender_id=current_user.id,
        receiver_id=receiver.id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return db_message


@message_router.get("/conversations", response_model=List[Dict[str, Any]])
def view_conversations(
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)):  
    
    return message_service.view_conversations(db, current_user.id)


@message_router.get("/conversation/{user_id}")
def view_conversation(
    user_id: int,
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)):

    return message_service.view_conversation(db, current_user.id, user_id)
    