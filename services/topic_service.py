from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateTopicRequest, Topic, User
from services.user_service import check_admin_role


def create_topic(db: Session, topic: CreateTopicRequest, current_user: User):
    db_topic = Topic(title=topic.title, author_id=current_user.id, category_id=topic.category_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topics(db: Session,
               skip: int = 0,
               limit: int = 100,
               sort: str = None or None,
               search: str = None or None):
    topics = db.query(Topic)
    if search:
        topics = topics.filter(Topic.title.contains(search))
    if sort:
        if sort.lower() == "desc":
            topics = topics.order_by(desc(Topic.id))
        elif sort.lower() == "asc":
            topics = topics.order_by(asc(Topic.id))
    topics = topics.offset(skip).limit(limit).all()
    return topics


def get_topic(db: Session, topic_id: int):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is not None:
        author = db.query(User).get(topic.author_id)
        return {"topic": topic, "author": author}
    else:
        return None
    

def lock_topic_for_users(db: Session, topic_id: int, current_user):
    check_admin_role(current_user)
    topic = db.query(Topic).get(topic_id)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Topic not found.")
    topic.is_locked = True
    db.commit()
    return topic