from fastapi import HTTPException, status
from auth.models import User
from auth.roles import Roles


def create_token(user_data):
    pass


def register_user(user_data):
    pass


def view_privilaged_users():
    pass


def check_admin_role(current_user: User):
    if current_user.role != Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="The user is not authorized to perform this action.")