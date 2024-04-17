from fastapi import APIRouter


router = APIRouter()


@router.get("/categories")
def view_categories():
    pass


@router.get("/category/{category_id}")
def view_category(category_id: int):
    pass