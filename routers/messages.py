from fastapi import APIRouter


router = APIRouter()


@router.post("/message")
def create_message():
    pass


@router.get("/conversations")
def view_conversations():
    pass


@router.get("/conversation/{user_id}")
def view_conversation(user_id: int):
    pass