from fastapi import Depends, HTTPException, status
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session
from data.models import CategoryAccess, CreateCategoryRequest, Category, Topic, User
from auth.token import get_current_user
from data.database import get_db
from data.roles import Roles
from services.user_service import check_admin_role


def create_category(db: Session, category: CreateCategoryRequest,
                    current_user: User = Depends(get_current_user)):
    check_admin_role(current_user)
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int, current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category not found.")
    if category.is_private:
        if current_user.role == Roles.admin:
            return category
        access = db.query(CategoryAccess).filter_by(
            category_id=category_id,
            user_id=current_user.id,
            read_access=True).first()
        if not access:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                                detail="Access to the category is restricted.")
    return category


def get_categories(db: Session, current_user: User = Depends(get_current_user),
               skip: int = 0,
               limit: int = 100,
               sort: str = None,
               search: str = None):
    if current_user.role == Roles.admin:
        categories = db.query(Category)
    else:
        categories = db.query(Category).outerjoin(
            CategoryAccess, 
            (CategoryAccess.category_id == Category.id) & 
            (CategoryAccess.user_id == current_user.id)).filter(or_(Category.is_private == False, CategoryAccess.read_access == True))
    if search:
        categories = categories.filter(Category.name.contains(search))
    if sort:
        if sort.lower() == "desc":
            categories = categories.order_by(desc(Category.id))
        elif sort.lower() == "asc":
            categories = categories.order_by(asc(Category.id))
    categories = categories.offset(skip).limit(limit).all()
    return categories


def get_topics_in_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    topics = db.query(Topic).filter(Topic.category_id == category_id).offset(skip).limit(limit).all()
    if not topics:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No topics found in the category.")
    return topics


def toggle_category_visibility(category_id: int, db: Session = Depends(get_db), 
                               current_user: User = Depends(get_current_user)):
    check_admin_role(current_user)
    category = get_category(db, category_id, current_user)
    category.is_private = not category.is_private
    db.commit()
    return {"message": f"Visibility for category '{category.name}' changed to {'private' if category.is_private else 'public'}.",
            "category": {"id": category.id, 
                         "name": category.name, 
                         "is_private": category.is_private}}


def check_if_private(category: Category):
    if not category.is_private:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="The category is public.")


# Check if the user exists, currently non-existent users
# can get read access to a category
def read_access(db: Session, category_id: int, user_id: int,
                current_user: User = Depends(get_current_user)):
    check_admin_role(current_user)
    category = get_category(db, category_id, current_user)
    check_if_private(category)
    access_record = db.query(CategoryAccess).filter_by(category_id=category_id, user_id=user_id).first()
    if access_record is None:
        access_record = CategoryAccess(category_id=category_id, user_id=user_id, read_access=True)
        db.add(access_record)
    else:
        access_record.read_access = True
    db.commit()
    return {"message": "Read permission has been granted."}


# Check if the user exists, currently non-existent users
# can get write access to a category
def write_access(db: Session, category_id: int, user_id: int,
                 current_user: User = Depends(get_current_user)):
    check_admin_role(current_user)
    category = get_category(db, category_id, current_user)
    check_if_private(category)
    access_record = db.query(CategoryAccess).filter_by(category_id=category_id, user_id=user_id).first()
    if access_record is None:
        access_record = CategoryAccess(category_id=category_id, user_id=user_id, read_access=True, write_access=True)
        db.add(access_record)
    else:
        access_record.read_access = True
        access_record.write_access = True
    db.commit()
    return {"message": "Write permission has been granted."}


def revoke_user_access(db: Session, category_id: int, user_id: int, access_type: str,
                       current_user: User = Depends(get_current_user)):
    check_admin_role(current_user)
    access_record = db.query(CategoryAccess).filter_by(category_id=category_id, user_id=user_id).first()
    if access_record is None or (not access_record.read_access and not access_record.write_access):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user does not have any permissions.")
    if access_type == "read":
        access_record.read_access = False
        access_record.write_access = False
    elif access_type == "write" and access_record.write_access:
        access_record.write_access = False
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid access type.")
    db.commit()
    return {"message": f"The user's {access_type} access has been revoked."}


# Eventually implement unlock
def lock_category_for_users(category_id: int, current_user, db: Session):
    check_admin_role(current_user)
    category = db.query(Category).get(category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category not found.")
    category.is_locked = True
    db.commit()
    return {"message": "Category has been locked."}