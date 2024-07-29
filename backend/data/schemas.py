from pydantic import BaseModel, validator, conint


class CreateUserRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class CreateTopicRequest(BaseModel):
    title: str
    category_id: int


class CreateCategoryRequest(BaseModel):
    name: str


class CreateMessageRequest(BaseModel):
    text: str
    receiver_id: int


class CreateReplyRequest(BaseModel):
    content: str
    topic_id: int


class CreateVoteRequest(BaseModel):
    vote_type: conint(ge=-1, le=1) # type: ignore

    @validator("vote_type")
    def check_vote_type(cls, value):
        if value not in (-1, 1):
            raise ValueError("vote_type must be either -1 (downvote) or 1 (upvote).")
        return value