from sqlalchemy.orm import Session
from auth.database import SessionLocal, engine, Base
from auth.models import Users

def seed_database():
    db = SessionLocal()
    users = [
        Users(username="Koko", hashed_password="123456"),
        Users(username="Alex", hashed_password="789456")
    ]

    db.add_all(users)
    db.commit()
    db.close()
    print("Database seeded successfully")


if __name__ == "__main__":
    seed_database()
