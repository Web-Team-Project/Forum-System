from fastapi import Depends, HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateCategoryRequest, Category, Roles, Users
from auth.token import get_current_user


def create_category(db: Session, category: CreateCategoryRequest, 
                    current_user: 
                    Users = Depends(get_current_user)): 
    # Warning! Must think about implementing admin and his privileges
    if current_user.role != Roles.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The user is not authorized to create a category.")
    db_category = Category(name=category.name, admin=current_user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session,
               skip: int = 0,
               limit: int = 100,
               sort: str = None or None,
               search: str = None or None):
    
    categories = db.query(Category)
    if search:
        categories = categories.filter(Category.name.contains(search))
    if sort:
        if sort.startswith("-"):
            sort = sort[1:]
            categories = categories.order_by(desc(sort))
        else:
            categories = categories.order_by(asc(sort))
    categories = categories.offset(skip).limit(limit).all()
    return categories


def get_category(db: Session, topic_id: int):
    topic = db.query(Category).filter(Category.id == topic_id).first()
    if topic is not None:
        author = db.query(Users).get(category.admin)
        return {"topic": topic, "author": author}
    else:
        return None