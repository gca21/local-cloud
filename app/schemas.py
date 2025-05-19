from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Annotated
from datetime import datetime


class UserBase(BaseModel):
    id: Annotated[int, Field(description="Unique identifier of the user")]
    username: Annotated[str, Field(description="Unique name of the user")]
    password: Annotated[str, Field(description="Password of the user")]
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    username: Annotated[str, Field(description="Unique name of the user")]
    password: Annotated[str, Field(description="Password of the user")]

class ItemBase(BaseModel):
    id: Annotated[str, Field(description="Unique identifier of the item")]
    name: Annotated[str, Field(description="Name of the item")]
    is_dir: Annotated[bool, Field(description="Wether an item is a directory or not")]
    parent_id: Annotated[str | None, Field(default=None, description="Unique identifier of the parent item")]
    path: Annotated[str, Field(description="Item relative path in the uploads folder")]
    size: Annotated[int | None, Field(default=None, description="File size in bytes")]
    mimetype: Annotated[str | None, Field(default=None, description="Mimetype of the file")]
    created_at: Annotated[datetime, Field(description="Creation date of the item")]
    updated_at: Annotated[datetime, Field(description="Update date of the item")]
    
    #parent: Annotated[Optional['ItemBase'], Field(description="Parent item")]
    children: Annotated[Optional[list['ItemBase']], Field(default=[], description="List of the children of the directory")]
    
    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    name: Annotated[str, Field(description="Name of the item")]
    is_dir: Annotated[bool, Field(description="Wether an item is a directory or not")]
    parent_id: Annotated[str | None, Field(default=None, description="Unique identifier of the parent item")]
    size: Annotated[int | None, Field(default=None, description="File size in bytes")]

class ItemUpdate(BaseModel):
    id: Annotated[str, Field(description="Unique identifier of the item")]
    name: Annotated[str | None, Field(default=None, description="Name of the item")]
    parent_id: Annotated[str | None, Field(default=None, description="Unique identifier of the parent item")]
