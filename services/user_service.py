from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from auth.models import Category, CategoryAccess, User
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
    

def has_write_access(db: Session, category_id: int, user_id: int):
    category = db.query(Category).filter_by(id=category_id).first()
    if category.is_private:
        access_record = db.query(CategoryAccess).filter_by(category_id=category_id, user_id=user_id).first()
        if not access_record or not access_record.write_access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have the needed permissions.")