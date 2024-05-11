from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from data.database import get_db
from data.models import CreateMessageRequest, Message, User
from auth.token import get_current_user
from services.message_service import get_conversations, get_conversation


message_router = APIRouter(prefix="/messages", tags=["messages"])


@message_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_message(message: CreateMessageRequest,
                       current_user: User = Depends(get_current_user), 
                       db: Session = Depends(get_db)):  
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if receiver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Receiver not found.")
    db_message = Message(text=message.text, 
                         sender_id=current_user.id, 
                         receiver_id=receiver.id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@message_router.get("/conversations")
def view_conversations(current_user: User = Depends(get_current_user), 
                       db: Session = Depends(get_db)):  
    return get_conversations(db, current_user.id)


@message_router.get("/conversation/{user_id}")
def view_conversation(user_id: int, 
                      current_user: User = Depends(get_current_user), 
                      db: Session = Depends(get_db)):
    return get_conversation(db, current_user.id, user_id)