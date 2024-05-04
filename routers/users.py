from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.token import get_current_user
from data.database import get_db
from data.models import User
from data.roles import Roles
from services.user_service import check_admin_role


users_router = APIRouter(prefix="/users", tags=["users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@users_router.post("/token")
def login():
    pass


@users_router.post("/register")
def register():
    pass


@users_router.get("/user_info", status_code=status.HTTP_200_OK)
async def user_info(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Authentication has failed.")
    return {"user": user}


@users_router.put("/{user_id}/role", status_code=status.HTTP_200_OK)
def update_user_role(user_id: int, 
                     new_role: Roles, 
                     current_user: User = Depends(get_current_user), 
                     db: Session = Depends(get_db)):
    check_admin_role(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User with not found.")
    user.role = new_role
    db.commit()
    return {"message": f"User role updated to {new_role.value}."}