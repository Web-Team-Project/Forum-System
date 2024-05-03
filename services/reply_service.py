from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from auth.models import CreateReplyRequest, Reply, Vote, Topic
from services.user_service import has_write_access


def create_reply(db: Session, reply_req: CreateReplyRequest, current_user):
    topic = db.query(Topic).get(reply_req.topic_id)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Topic not found.")
    if topic.is_locked:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="The topic is locked.")
    has_write_access(db, topic.category_id, current_user.id)
    new_reply = Reply(content=reply_req.content, 
                      user_id=current_user.id, 
                      topic_id=reply_req.topic_id)
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def add_or_update_vote(db: Session, user_id: int, reply_id: int, vote_type: int):
    existing_vote = db.query(Vote).filter_by(user_id=user_id, reply_id=reply_id).first()
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            return existing_vote, "You have already voted in this way."
        existing_vote.vote_type = vote_type
        created_vote = False
    else:
        reply = db.query(Reply).filter_by(id=reply_id).first()
        if not reply:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="Reply not found.")
        new_vote = Vote(user_id=user_id, reply_id=reply_id, vote_type=vote_type)
        db.add(new_vote)
        existing_vote = new_vote
        created_vote = True
    db.commit()
    if created_vote:
        return existing_vote, "Vote has been registered."
    else:
        return existing_vote, "Vote has been updated."


def add_best_reply(db: Session, topic_id: int, reply_id: int, user_id: int):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Topic not found.")
    if topic.author_id != user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Only the topic author can set the best reply.")
    reply = db.query(Reply).filter(Reply.id == reply_id, Reply.topic_id == topic_id).first()
    if not reply:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Reply not found.")
    db.query(Reply).filter(Reply.topic_id == topic_id).update({Reply.is_best_reply:False})
    reply.is_best_reply = True
    topic.best_reply_id = reply_id
    db.commit()
    db.refresh(reply)
    return reply