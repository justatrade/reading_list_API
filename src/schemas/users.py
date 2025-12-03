from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    display_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    display_name: Optional[str] = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
