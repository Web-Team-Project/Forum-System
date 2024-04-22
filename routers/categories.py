from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.models import Category, CreateCategoryRequest, Topics, Users
from auth.database import get_db
from auth.token import get_current_user


category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(category: CreateCategoryRequest, 
                    current_user: Users = Depends(get_current_user), 
                    db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    db_category = Category(name=category.name)
    db.add(db_category)
    try:
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Category already exists")
    return {"category": db_category.name}


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