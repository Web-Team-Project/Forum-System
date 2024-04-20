from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.token import get_current_user
from auth.database import get_db
from auth.models import Users, CreateTopicRequest, Topic
from services import topic_service


topics_router = APIRouter(prefix="/topics", tags=["topics"])


@topics_router.post("/", response_model=Topic, status_code=status.HTTP_201_CREATED)
async def create_topic(topic: CreateTopicRequest,
                        current_user: Users = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return topic_service.create_topic(db, topic, current_user)


@topics_router.get("/")
async def view_topics(skip: int = 0,
                      limit: int = 100,
                      sort: str = None or None,
                      search: str = None or None,
                      db: Session = Depends(get_db)):
    topics = topic_service.get_topics(db, skip=skip, limit=limit, sort=sort, search=search)
    return topics


@topics_router.get("/{topic_id}", response_model=Topic)
async def view_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = topic_service.get_topic(db, topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic