from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from auth.models import CreateCategoryRequest, Category, Users


def create_category(db: Session, category: CreateCategoryRequest, admin: dict): #Warning must think about implementing admin and his privileges
    db_topic = Category(name=category.name, admin=admin["id"])
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def get_categories(db: Session,      #???
               skip: int = 0,        #???
               limit: int = 100,     #???
               sort: str = None or None,    #???
               search: str = None or None):   #???
    
    categories = db.query(Category)
    if search:                                     #!!! should think about searches for categories or someother way for finding them
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