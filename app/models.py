from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from datetime import datetime, timezone
from typing import Optional
import uuid

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

class Item(Base):
    __tablename__ = "items"
    
    id: Mapped[str] = mapped_column(primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str]
    is_dir: Mapped[bool]
    parent_id: Mapped[Optional[str]] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), nullable=True,)
        
    path: Mapped[str] = mapped_column(unique=True)
    size: Mapped[Optional[int]] # NULL for directories
    mimetype: Mapped[Optional[str]] # NULL for directories
    
    created_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    parent: Mapped[Optional["Item"]] = relationship(back_populates="children", remote_side=[id])
    children: Mapped[list["Item"]] = relationship(back_populates="parent", cascade="all, delete-orphan")
    