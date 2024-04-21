from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from auth.models import CreateTopicRequest, Users
from auth.token import get_current_user
from services import category_service
from auth.database import get_db

category_router = APIRouter(prefix="/categories", tags=["categories"])

@category_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_topic(topic: CreateTopicRequest,
                        current_user: Users = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return category_service.create_category(db, category, admin)  #???

@category_router.get("/")
async def view_categories(db: Session = Depends(get_db)):
    categories = category_service.get_categories(db)  # Using function from category_service
    return categories

@category_router.get("/{category_id}")
async def view_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)  # Using function from category_service
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"category": category, "topics": category.topics}