from auth.token import get_current_user
from data.models import Category, CategoryAccess, Reply, Topic, User
from data.roles import Roles
from data.schemas import CreateTopicRequest
from fastapi import Depends, HTTPException, status
from services.user_service import check_admin_role, has_write_access
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session


def create_topic(db: Session, topic: CreateTopicRequest, current_user: User):
    has_write_access(db, topic.category_id, current_user.id)
    db_topic = Topic(
        title=topic.title, author_id=current_user.id, category_id=topic.category_id
    )
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_topics(
    db: Session,
    skip: int = 0,  # Sets the number of topics to skip until we reach the desired page
    limit: int = 100,  # Sets the maximum number of topics to be returned
    sort: str = None,
    search: str = None,
    current_user: User = Depends(get_current_user),
):
    topics = db.query(Topic).join(Category, Topic.category_id == Category.id)
    if current_user.role != Roles.admin:
        topics = topics.outerjoin(
            CategoryAccess,
            (CategoryAccess.category_id == Topic.category_id)
            & (CategoryAccess.user_id == current_user.id),
        ).filter(or_(Category.is_private is False, CategoryAccess.read_access is True))
    if search:
        topics = topics.filter(Topic.title.contains(search))
    if sort:
        if sort.lower() == "desc":
            topics = topics.order_by(desc(Topic.id))
        elif sort.lower() == "asc":
            topics = topics.order_by(asc(Topic.id))
    topics = topics.offset(skip).limit(limit).all()
    return topics


def get_topic(db: Session, topic_id: int, current_user):
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is not None:
        if (
            not current_user.role == Roles.admin
            and topic.category.is_private
            and db.query(CategoryAccess)
            .filter_by(
                category_id=topic.category_id, user_id=current_user.id, read_access=True
            )
            .first()
            is None
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to view this topic.",
            )
        author = db.query(User).get(topic.author_id)
        replies = db.query(Reply).filter(Reply.topic_id == topic_id).all()
        return {"topic": topic, "author": author, "replies": replies}
    else:
        return None


# Eventually implement unlock
def lock_topic_for_users(db: Session, topic_id: int, current_user):
    check_admin_role(current_user)
    topic = db.query(Topic).get(topic_id)
    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found."
        )
    topic.is_locked = True
    db.commit()
    return {"message": "Topic has been locked."}
