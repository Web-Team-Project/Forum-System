from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateTopicRequest, Topics, Users


def create_topic(db: Session, topic: CreateTopicRequest, current_user: Users):
    db_topic = Topics(title=topic.title, author_id=current_user.id, category_id=topic.category_id)
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
        if sort.lower() == "desc":
            topics = topics.order_by(desc(Topics.id))
        elif sort.lower() == "asc":
            topics = topics.order_by(asc(Topics.id))
    topics = topics.offset(skip).limit(limit).all()
    return topics


def get_topic(db: Session, topic_id: int):
    topic = db.query(Topics).filter(Topics.id == topic_id).first()
    if topic is not None:
        author = db.query(Users).get(topic.author_id)
        return {"topic": topic, "author": author}
    else:
        return None