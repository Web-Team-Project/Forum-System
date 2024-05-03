from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from data_folder.models import CategoryAccess, CreateTopicRequest, Topic, User
from data_folder.roles import Roles
from services.user_service import check_admin_role, has_write_access


def create_topic(db: Session, topic: CreateTopicRequest, current_user: User):
    has_write_access(db, topic.category_id, current_user.id)
    db_topic = Topic(title=topic.title, author_id=current_user.id, category_id=topic.category_id)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topics(db: Session,
               skip: int = 0,
               limit: int = 100,
               sort: str = None or None,
               search: str = None or None,
               current_user: User = None):
    topics = db.query(Topic)
    if search:
        topics = topics.filter(Topic.title.contains(search))
    if sort:
        if sort.lower() == "desc":
            topics = topics.order_by(desc(Topic.id))
        elif sort.lower() == "asc":
            topics = topics.order_by(asc(Topic.id))
    if current_user:
        topics = topics.join(CategoryAccess, Topic.category_id == CategoryAccess.category_id) \
                       .filter(CategoryAccess.user_id == current_user.id, CategoryAccess.read_access == True)
    topics = topics.offset(skip).limit(limit).all()
    return topics


def get_topic(db: Session, topic_id: int, current_user):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is not None:
        if not current_user.role == Roles.admin and topic.category.is_private and \
            db.query(CategoryAccess).filter_by(category_id=topic.category_id, user_id=current_user.id, read_access=True).first() is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="You are not allowed to view this topic.")
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
    return {"topic": topic, "message": "Topic has been locked."}