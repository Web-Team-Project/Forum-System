from fastapi import APIRouter


router = APIRouter()


@router.post("/reply")
def create_reply():
    pass


@router.post("/reply/{reply_id}/upvote")
def upvote_reply(reply_id: int):
    pass


@router.post("/reply/{reply_id}/downvote")
def downvote_reply(reply_id: int):
    pass