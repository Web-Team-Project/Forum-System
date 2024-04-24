from typing import Dict, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from auth.models import CreateMessageRequest, Message, Users
from datetime import datetime

def create_message(db: Session, message: CreateMessageRequest, sender_id: int, receiver_id: int):
    db_message = Message(
        text=message.text,
        sender_id = sender_id,
        receiver_id = receiver_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def view_conversations(db: Session, current_user_id: int) -> List[Dict]:
    messages = db.query(Message).filter(Message.sender_id == current_user_id).all()
    formatted_messages = []
    for message in messages:
        sender_username = db.query(Users.username).filter(Users.id == message.sender_id).scalar()
        receiver_username = db.query(Users.username).filter(Users.id == message.receiver_id).scalar()
        formatted_message = {
            "sender": sender_username,
            "receiver": receiver_username,
            "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
            "text": message.text
        }
        formatted_messages.append(formatted_message)
    return formatted_messages


def view_conversation(db: Session, current_user_id: int, user_id: int):
    receiver = db.query(Users).filter(Users.id == user_id).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="User not found.")
    
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user_id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user_id))
    ).order_by(Message.sent_at).all()
    formatted_messages = []
    for message in messages:
        sender_username = db.query(Users.username).filter(Users.id == message.sender_id).scalar()
        receiver_username = db.query(Users.username).filter(Users.id == message.receiver_id).scalar()
        formatted_message = {
            "sender": sender_username,
            "receiver": receiver_username,
            "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
            "text": message.text
        }
        formatted_messages.append(formatted_message)
    return formatted_messages