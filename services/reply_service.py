from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.models import CreateReplyRequest, Reply, Users
from auth.token import get_current_user


def create_reply(db: Session, reply_req: CreateReplyRequest, current_user):
    new_reply = Reply(
        content=reply_req.content,
        user_id=current_user.id,
        topic_id=reply_req.topic_id
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply

# def create_category(db: Session, category: CreateCategoryRequest, current_user: Users = Depends(get_current_user)):
#     # Warning! Must think about implementing admin and his privileges
#     db_category = Category(name=category.name)
#     db.add(db_category)
#     db.commit()
#     db.refresh(db_category)
#     return db_category

def upvote_reply(reply_id):
    pass

def downvote_reply(reply_id):
    pass