from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from auth.models import CreateReplyRequest, Users, Topics, Vote, CreateVote, Reply
from auth.database import get_db
from auth.token import get_current_user
from services.reply_service import create_reply, add_or_update_vote, set_best_reply


reply_router = APIRouter(prefix="/replies", tags=["replies"])


@reply_router.post("/", status_code=status.HTTP_201_CREATED)
def create_reply_route(reply: CreateReplyRequest,
        current_user: Users = Depends(get_current_user),
        db: Session =Depends(get_db)):

    return create_reply(db, reply, current_user)


@reply_router.post("/replies/{reply_id}/vote")
def vote_reply(reply_id: int,
               vote_data: CreateVote,
               db: Session = Depends(get_db),
               current_user: Users = Depends(get_current_user)):
    vote = add_or_update_vote(db, current_user.id, reply_id, vote_data.vote_type)
    return {"message": "Vote registered"}


@reply_router.post("/replies/{reply_id}/set-best")
def set_best_reply_route(
        topic_id: int,
        reply_id: int,
        db: Session = Depends(get_db),
        current_user: Users = Depends(get_current_user)):
    result = set_best_reply(db, topic_id, reply_id, current_user.id)
    return {"message": "Best of reply set successfully", "reply_id": result.id}

