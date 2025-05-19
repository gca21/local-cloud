from fastapi import APIRouter
from fastapi import Depends
from app.schemas import ItemBase
from app.dependencies import get_db, get_item_dao
from sqlalchemy.orm import Session
from app.crud.item import ItemDAO

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("", response_model=list[ItemBase])
def read_all_items(db: Session = Depends(get_db), item_dao: ItemDAO = Depends(get_item_dao)):
    return item_dao.read_all_items(db)