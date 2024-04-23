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

def view_conversations(db: Session):
    # Implement logic to retrieve conversations from the database
    pass

def view_conversation(db: Session, user_id: int):
    # Implement logic to retrieve conversation with user_id from the database
    pass
