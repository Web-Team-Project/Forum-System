from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.models import Category, Topics
from auth.database import get_db


category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category():
    pass


@category_router.get("/categories/{category_id}")
def view_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category not found.")
    topics = db.query(Topics).filter(Topics.category_id == category_id).all()
    return {"category": category.name, "topics": [topic.title for topic in topics]}


@category_router.get("/categories")
def view_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return {"categories": [category.name for category in categories]}