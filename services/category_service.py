from fastapi import Depends, HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateCategoryRequest, Category, Topic, User
from auth.roles import Roles
from auth.token import get_current_user


def create_category(db: Session, category: CreateCategoryRequest, 
                    current_user: User = Depends(get_current_user)):
    if current_user.role != Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user is not authorized to create a category.")
    db_category = Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")
    return category


def get_categories(db: Session,
               skip: int = 0,
               limit: int = 100,
               sort: str = None,
               search: str = None):
    categories = db.query(Category)
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
    if topics is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    return topics