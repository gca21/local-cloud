from sqlalchemy import select, insert
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import User

def username_exists(db: Session, username: str) -> bool:
    stmt = select(User).where(User.username == username)
    result = db.execute(stmt).first()
    return result is not None

def read_user(db: Session, id: int) -> User | None:
    stmt = select(User).where(User.id == id)
    result = db.execute(stmt).first()
    if result is None:
        return None
    return result[0]

def create_user(db: Session, username: str, hashed_password: str) -> User | None:
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise 
    return new_user

def update_user(db: Session, id: int, username: str | None = None, hashed_password: str | None = None) -> User | None:
    user = read_user(db, id)
    if user is None:
        return None
    
    if username is not None:
        user.username = username
    if hashed_password is not None:
        user.password = hashed_password
    
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise
    
    return user

def delete_user(db: Session, id: int) -> User | None:
    user = db.get(User, id)
    if user is None:
        return None
    
    db.delete(user)
    db.commit()
    return user
    