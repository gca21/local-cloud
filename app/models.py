from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_dir = Column(Boolean, nullable=False)
    parent_id = Column(Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=True)
    
    path = Column(String, unique=True)
    size = Column(Integer, nullable=True)
    mimetype = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    children = relationship("Item", backref="parent", remote_side=[id], cascade="all, delete-orphan")
    