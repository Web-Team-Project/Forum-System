from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateCategoryRequest, Category, Topics


def create_category(db: Session, category: CreateCategoryRequest): 
    # Warning! Must think about implementing admin and his privileges
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


def get_topics_in_category(db: Session, category_id: int, skip: int = 0, limit: int = 100):
    topics = db.query(Topics).filter(Topics.category_id == category_id).offset(skip).limit(limit).all()
    if topics is None:
        raise HTTPException(status_code=404, detail="Category not found.")
    return topics