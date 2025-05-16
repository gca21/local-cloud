from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from app.models import User

def username_exists(db: Session, username: str) -> bool:
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt).first()
    return result is not None
