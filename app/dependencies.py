from app.database import SessionLocal
from app.crud.item import ItemDAO
from app.uploads_manager import UploadsManager

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_item_dao():
    return ItemDAO()

def get_uploads_manager():
    return UploadsManager()