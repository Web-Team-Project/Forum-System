from typing import Annotated

from auth.token import get_current_user
from data.database import get_db
from data.models import User
from data.roles import Roles
from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import check_admin_role
from sqlalchemy.orm import Session

users_router = APIRouter(prefix="/users", tags=["users"])

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@users_router.get("/info", status_code=status.HTTP_200_OK)
async def user_info(user: user_dependency, db: db_dependency):
    if user:
        return {"user": user}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not authenticated."
        )


@users_router.put("/{user_id}/role", status_code=status.HTTP_200_OK)
def update_user_role(
    user_id: int,
    new_role: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    check_admin_role(current_user)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    role_value = new_role.get("new_role")
    if role_value not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role."
        )
    user.role = Roles(role_value)
    db.commit()
    return {"message": f"User role updated to {role_value}."}
