from pydantic import BaseModel, Field
from typing import Optional, Annotated


class UserBase(BaseModel):
    id: Annotated[int, Field(description="Unique identifier of the user")]
    username: Annotated[str, Field(description="Unique name of the user")]
    password: Annotated[str, Field(description="Password of the user")]
    
    class Config:
        from_attributes=True

class UserCreate(BaseModel):
    username: Annotated[str, Field(description="Unique name of the user")]
    password: Annotated[str, Field(description="Password of the user")]