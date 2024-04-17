from fastapi import APIRouter


router = APIRouter()


@router.post("/token")
def login():
    pass


@router.post("/register")
def register():
    pass