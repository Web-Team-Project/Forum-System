from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.models import CreateReplyRequest, Reply, Users, Vote
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


def add_or_update_vote(db: Session, user_id: int, reply_id: int, vote_type: int) -> Vote:
    existing_vote = db.query(Vote).filter_by(user_id=user_id, reply_id=reply_id).first()
    if existing_vote:
        existing_vote.vote_type = vote_type
    else:
        # Make sure the reply exists
        reply = db.query(Reply).filter_by(id=reply_id).first()
        if not reply:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reply not found")
        new_vote = Vote(user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        db.add(new_vote)
        existing_vote = new_vote
    db.commit()
    return existing_vote