from auth.token import get_current_user
from data.database import get_db
from data.models import User
from data.schemas import CreateCategoryRequest
from fastapi import APIRouter, Depends, status
from services.category_service import (
    create_category,
    get_categories,
    get_category,
    get_topics_in_category,
    lock_category_for_users,
    read_access,
    revoke_user_access,
    toggle_category_visibility,
    write_access,
)
from services.user_service import privileged_users
from sqlalchemy.orm import Session

category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_category(
    category: CreateCategoryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_category(db, category, current_user)


@category_router.get("/{category_id}")
def view_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = get_category(db, category_id, current_user)
    topics = get_topics_in_category(db, category_id)
    return {"category": category.name, "topics": [topic.title for topic in topics]}


@category_router.get("/")
def view_categories(
    skip: int = 0,
    limit: int = 100,
    sort: str = None,
    search: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_categories(
        db, current_user, skip=skip, limit=limit, sort=sort, search=search
    )


@category_router.put("/{category_id}/visibility")
def change_visibility(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return toggle_category_visibility(category_id, db, current_user)


@category_router.put("/{category_id}/users/{user_id}/read-access")
def give_read_access(
    category_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return read_access(db, category_id, user_id, current_user)


@category_router.put("/{category_id}/users/{user_id}/write-access")
def give_write_access(
    category_id: int,
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return write_access(db, category_id, user_id, current_user)


@category_router.put("/{category_id}/users/{user_id}/access/{access_type}")
def revoke_access(
    category_id: int,
    user_id: int,
    access_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return revoke_user_access(db, category_id, user_id, access_type, current_user)


@category_router.get("/privileged-users/{category_id}")
def view_privileged_users(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return privileged_users(db, category_id, current_user)


@category_router.put("/lock/{category_id}")
def lock_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return lock_category_for_users(category_id, current_user, db)
