from typing import Dict, List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from auth.models import CreateMessageRequest, Message, User


def create_message(db: Session, message: CreateMessageRequest, sender_id: int, receiver_id: int):
    db_message = Message(text=message.text, 
                         sender_id = sender_id, 
                         receiver_id = receiver_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def format_date(date):
    formatted_date = date.strftime("%d %b %Y, %H:%M")
    day = int(date.strftime("%d"))
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    formatted_date = formatted_date.replace(date.strftime("%d"), f"{day}{suffix}")
    return formatted_date


def format_message(message, db: Session):
    sender_username = db.query(User.username).filter(User.id == message.sender_id).scalar()
    receiver_username = db.query(User.username).filter(User.id == message.receiver_id).scalar()
    formatted_message = {
        "sender": sender_username,
        "receiver": receiver_username,
        "sent_at": format_date(message.sent_at),
        "text": message.text
    }
    return formatted_message


def get_conversations(db: Session, current_user_id: int) -> List[Dict]:
    messages = db.query(Message).filter(Message.sender_id == current_user_id).all()
    formatted_messages = [format_message(message, db) for message in messages]
    return formatted_messages


def get_conversation(db: Session, current_user_id: int, user_id: int):
    receiver = db.query(User).filter(User.id == user_id).first()
    if receiver is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Receiver not found.")
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.sent_at).all()
    formatted_messages = [format_message(message, db) for message in messages]
    return formatted_messages