from auth.token import get_current_user
from data.database import get_db
from data.models import User
from data.schemas import CreateReplyRequest, CreateVoteRequest
from fastapi import APIRouter, Depends, status
from services.reply_service import add_best_reply, add_or_update_vote, create_reply
from sqlalchemy.orm import Session

reply_router = APIRouter(prefix="/replies", tags=["replies"])


@reply_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_reply(
    reply: CreateReplyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_reply(db, reply, current_user)


@reply_router.post("/{reply_id}/vote")
def vote_reply(
    reply_id: int,
    vote_data: CreateVoteRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _, message = add_or_update_vote(db, current_user.id, reply_id, vote_data.vote_type)
    return {"message": message}


@reply_router.post("/{reply_id}/best-reply")
def set_best_reply(
    topic_id: int,
    reply_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = add_best_reply(db, topic_id, reply_id, current_user.id)
    return {"message": "Best reply set successfully.", "reply_id": result.id}
