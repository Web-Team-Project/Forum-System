from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from auth.database import get_db
from auth.models import CreateMessageRequest, Message, Users
from auth.token import get_current_user
from services import message_service

message_router = APIRouter(prefix="/message", tags=["Messages"])


@message_router.post("/")
def create_message(
    message: CreateMessageRequest,
    current_user: Users = Depends(get_current_user),
    # user_receiver_id: Users = Depends(get_user),    #must create get_user to verify the existance of user (receiver)
    db: Session = Depends(get_db)
):  
    return create_message(db, message, current_user)


@message_router.get("/conversations", response_model=List[Dict[str, Any]])
def view_conversations(
    current_user: Users = Depends(get_current_user),
    db: Session = Depends(get_db)
):  
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required")
    
    # Call the service function to retrieve and format conversations
    return message_service.view_conversations(db, current_user.id)


@message_router.get("/conversation/{user_id}")
def view_conversation(user_id: int):
    pass