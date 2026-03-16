from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ApplicationCreate(BaseModel):
    company_name: str
    position: str
    status: str
    deadline: Optional[date] = None
    notes: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: int
    company_name: str
    position: str
    status: str
    owner_id: int
    applied_at: datetime
    deadline: Optional[date] = None
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)