from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User, Item
from app.schemas import ItemCreate, ItemUpdate
import mimetypes

def build_path(db: Session, filename: str, parent_id: int | None) -> str:
    if parent_id is None:
        return f"uploads/{filename}"
    
    parent = db.get(Item, parent_id)
    if parent is None:
        raise ValueError(f"Parent item with id {parent_id} does not exist")
    
    return f"{parent.path}/{filename}"

def get_mimetype(path: str) -> str | None:
    type, _ = mimetypes.guess_type(path)
    return type

def read_item(db: Session, id: int) -> Item | None:
    item = db.get(Item, id)
    return item

def read_children(db: Session, parent_id: int) -> list[Item]:
    stmt = select(Item).where(Item.parent_id == parent_id)
    result = db.execute(stmt).scalars().all()
    return result

def read_all_items(db: Session) -> list[Item]:
    stmt = select(Item)
    result = db.execute(stmt).scalars().all()
    return result

def create_item(db: Session, new_item: ItemCreate) -> Item | None:
    new_path = build_path(db, new_item.name, new_item.parent_id)
    model_item = Item(
        name=new_item.name,
        is_dir=new_item.is_dir,
        parent_id=new_item.parent_id,
        path=new_path,
        size=new_item.size,
        mimetype=get_mimetype(new_path),
    )
    
    db.add(model_item)
    try:
        db.commit()
        db.refresh(model_item)
    except IntegrityError:
        db.rollback()
        raise 
    return model_item

# Calculates and assigns the path of the children recursively
def update_children_paths(db: Session, parent_id: int):
    children = read_children(db, parent_id)
    for child in children:
        child.path = build_path(db, child.name, child.parent_id)
        try:
            db.commit()
            db.refresh(child)
        except IntegrityError:
            db.rollback()
            raise
        
        if child.is_dir:
            update_children_paths(db, child.id)

def update_item(db: Session, item: ItemUpdate) -> Item | None:
    db_item = db.get(Item, item.id)
    if db_item is None:
        return None
    
    # Change name
    if item.name is not None:
        db_item.name = item.name
    
    # Change parent - Update path, update childrens path
    if item.parent_id is not None:
        # Check if new parent exists
        parent = db.get(Item, item.parent_id)
        if parent is None:
            return None
        # Update parent and paths
        db_item.parent_id = item.parent_id
        db_item.path = build_path(db, db_item.name, db_item.parent_id)
        try:
            db.commit()
            db.refresh(db_item)
        except IntegrityError:
            db.rollback()
            raise
        # Update children paths
        update_children_paths(db, db_item.parent_id)
    
    return db_item

def delete_item(db: Session, id: int) -> User | None:
    item = db.get(Item, id)
    if item is None:
        return None
    
    db.delete(item)
    db.commit()
    return item
        
    