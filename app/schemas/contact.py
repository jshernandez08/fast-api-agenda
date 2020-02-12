from typing import List, Optional
from datetime import datetime
from .base import InitModel
from pydantic import BaseModel, Field, EmailStr

class ContactCreate(InitModel):
    name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    email: EmailStr
    phone_numbers: List[str] = []

class ContactUpdate(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_numbers: Optional[List[str]] = None
    updated_at: datetime = datetime.utcnow()

class ContactInDb(ContactCreate):
    pass
