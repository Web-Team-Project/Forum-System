from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from data.models import Category, CategoryAccess, User
from data.roles import Roles


def privileged_users(db: Session, category_id: int, current_user: User):
    # Check if the category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category not found.")

    check_admin_role(current_user)

    category_accesses = db.query(CategoryAccess).filter(CategoryAccess.category_id == category_id).all()
    privileged_users = []
    for access in category_accesses:
        user = access.user
        access_level = {"read_access": access.read_access, "write_access": access.write_access}
        user_details = {"id": user.id, "username": user.username, "access_level": access_level}
        privileged_users.append(user_details)
    return {"privileged_users": privileged_users}


def verify_username(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    return user is not None


def check_admin_role(current_user: User):
    if current_user is None or current_user.role != Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="The user is not authorized to perform this action.")
    

def has_write_access(db: Session, category_id: int, user_id: int):
    category = db.query(Category).filter_by(id=category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with ID {category_id} not found.")
    if category.is_private:
        access_record = db.query(CategoryAccess).filter_by(category_id=category_id, user_id=user_id).first()
        if not access_record or not access_record.write_access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have the needed permissions.")