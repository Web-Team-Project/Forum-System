from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from auth.models import CreateReplyRequest, Users, Topics
from auth.database import get_db
from auth.token import get_current_user
from services.reply_service import create_reply


reply_router = APIRouter(prefix="/replies", tags=["replies"])


@reply_router.post("/", status_code=status.HTTP_201_CREATED)
def create_reply_route(reply: CreateReplyRequest,
        current_user: Users = Depends(get_current_user),
        db: Session =Depends(get_db)):

    return create_reply(db, reply, current_user)


# @router.post("/reply/{reply_id}/upvote")
# def upvote_reply(reply_id: int):
#     pass
#
#
# @router.post("/reply/{reply_id}/downvote")
# def downvote_reply(reply_id: int):
#     pass