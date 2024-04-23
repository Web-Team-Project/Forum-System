from typing import Dict, List
from sqlalchemy.orm import Session
from auth.models import CreateMessageRequest, Message, Users

def create_message(db: Session, message: CreateMessageRequest, current_user: Users, receiver: Users):
    db_message = Message(
        text=message.text,
        sender=current_user.id,
        receiver=receiver.id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def view_conversations(db: Session, current_user_id: int) -> List[Dict]:
    messages = db.query(Message).filter(Message.user_sender_id == current_user_id).all()

    # Format messages for display in UI
    formatted_messages = []
    for message in messages:
        sender_username = db.query(Users.username).filter(Users.id == message.user_sender_id).scalar()
        receiver_username = db.query(Users.username).filter(Users.id == message.user_reciever_id).scalar()
        formatted_message = {
            "sender": sender_username,
            "receiver": receiver_username,
            "sent_at": message.sent_at.strftime("%Y-%m-%d %H:%M:%S"),
            "text": message.text
        }
        formatted_messages.append(formatted_message)

    return formatted_messages

def view_conversation(db: Session, user_id: int):
    # Implement logic to retrieve conversation with user_id from the database
    pass
