from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from auth.models import CreateCategoryRequest, User
from auth.database import get_db
from auth.token import get_current_user
from services.category_service import create_category, get_categories, get_category, get_topics_in_category


category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_category(category: CreateCategoryRequest, 
                        current_user: User = Depends(get_current_user), 
                        db: Session = Depends(get_db)):
    return create_category(db, category, current_user)


@category_router.get("/{category_id}")
def view_category(category_id: int, db: Session = Depends(get_db)):
    category = get_category(db, category_id)
    topics = get_topics_in_category(db, category_id)
    return {"category": category.name, "topics": [topic.title for topic in topics]}


@category_router.get("/")
def view_categories(skip: int = 0, 
                    limit: int = 100, 
                    sort: str = None, 
                    search: str = None, 
                    db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit, sort=sort, search=search)