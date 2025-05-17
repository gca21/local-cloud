from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, Item
from app.schemas import ItemCreate

def build_path(db: Session, filename: str, parent_id: int | None) -> str:
    if parent_id is None:
        return f"uploads/{filename}"
    parent = db.get(Item, parent_id)
    return f"{parent.path}/{filename}"

def read_item(db: Session, id: int) -> Item:
    item = db.get(Item, id)
    return item

def read_all_items(db: Session) -> list[Item]:
    stmt = select(Item)
    result = db.execute(stmt).scalars().all()
    return result

def create_item(db: Session, new_item: ItemCreate) -> Item:
    model_item = Item(
        name=new_item.name,
        is_dir=new_item.is_dir,
        parent_id=new_item.parent_id,
        path=build_path(db, new_item.name, new_item.parent_id),
        size=new_item.size,
        mimetype=new_item.mimetype,
    )
    
    db.add(model_item)
    try:
        db.commit()
        db.refresh(model_item)
    except IntegrityError:
        db.rollback()
        raise 
    return model_item