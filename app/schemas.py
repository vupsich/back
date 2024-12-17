from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: str
    birth_date: date
    city: str
    language: str

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
