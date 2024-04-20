from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateTopicRequest, Topics, Users


def create_topic(db: Session, topic: CreateTopicRequest, current_user: dict):
    db_topic = Topics(title=topic.title, author_id=current_user["id"]) # Issue with author_id and the dict
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topics(db: Session,
               skip: int = 0,
               limit: int = 100,
               sort: str = None or None,
               search: str = None or None):
    
    topics = db.query(Topics)
    if search:
        topics = topics.filter(Topics.title.contains(search))
    if sort:
        if sort.startswith("-"):
            sort = sort[1:]
            topics = topics.order_by(desc(sort))
        else:
            topics = topics.order_by(asc(sort))

    topics = topics.offset(skip).limit(limit).all()
    return topics


def get_topic(db: Session, topic_id: int):
    topic = db.query(Topics).filter(Topics.id == topic_id).first()
    if topic is not None:
        author = db.query(Users).get(topic.author)
        return {"topic": topic, "author": author}
    else:
        return None