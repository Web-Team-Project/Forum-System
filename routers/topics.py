from fastapi import APIRouter


router = APIRouter()


@router.post("/topic")
def create_topic():
    pass


@router.get("/topics")
def view_topics():
    pass


@router.get("/topic/{topic_id}")
def view_topic(topic_id: int):
    pass