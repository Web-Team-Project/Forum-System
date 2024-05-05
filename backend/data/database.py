from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.base import Base


DATABASE_URL = "sqlite:///./forum.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from data.models import User, Token, Topic, Category, Message, Reply, Vote


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)