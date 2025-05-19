from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from fastapi.responses import FileResponse
from app.schemas import ItemBase, ItemCreate
from app.models import Item
from app.dependencies import get_db, get_item_dao, get_uploads_manager
from app.crud.item import ItemDAO
from app.uploads_manager import UploadsManager
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("", response_model=list[ItemBase])
def read_all_items(db: Session = Depends(get_db), item_dao: ItemDAO = Depends(get_item_dao)):
    return item_dao.read_all_items(db)

@router.post("", response_model=ItemBase)
async def create_item(
    name: Annotated[str, Form()],
    parent_id: Annotated[str | None, Form()] = None,
    file: Annotated[UploadFile, File()] = None,
    db: Session = Depends(get_db),
    item_dao: ItemDAO = Depends(get_item_dao),
    u_manager: UploadsManager = Depends(get_uploads_manager)
):
    # Reconstruct the pydantic schema
    item = ItemCreate(name=name, is_dir=(file is None), parent_id=parent_id)
    
    # Try to create the entry in the database
    try:
        db_item = item_dao.create_item(db, item)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Resource already exists")
    except ValueError:
        raise HTTPException(status_code=404, detail="Specified parent does not exist")
    
    # Store the actual file
    if not item.is_dir:
        file_content = await file.read()
        u_manager.create_or_update_file(db_item.id, file_content)
    
    return db_item

@router.delete("", response_model=ItemBase)
def remove_item(
    id: str,
    db: Session = Depends(get_db),
    item_dao: ItemDAO = Depends(get_item_dao),
    u_manager: UploadsManager = Depends(get_uploads_manager)
):
    
    db_item = item_dao.delete_item(db, id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item with that id doesn't exist")
    
    if not db_item.is_dir:
        u_manager.remove_file(id)
    else:
        remove_children_files(db_item, u_manager)
    return db_item

def remove_children_files(parent: Item, u_manager: UploadsManager):
    for child in parent.children:        
        if child.is_dir:
            remove_children_files(child, u_manager)
        else:
            u_manager.remove_file(child.id)

@router.get("{id}", response_class=FileResponse)
async def read_file(id: str, db: Session = Depends(get_db), item_dao: ItemDAO = Depends(get_item_dao)):
    db_item = item_dao.read_item(db, id)
    if db_item is None:
        return None
    return FileResponse(path=f"uploads/{db_item.id}", filename=db_item.name, media_type=db_item.mimetype)