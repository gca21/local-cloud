from app.database import SessionLocal
from app.crud.item import ItemDAO

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_item_dao():
    return ItemDAO()