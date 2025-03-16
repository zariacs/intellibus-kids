from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    id: int
    name: str 
    role: str
    email: EmailStr
    password: str
    nutri_code: Optional[str] = None

class CreateUser(BaseModel):
    name: str
    role: str
    email: EmailStr
    nutri_code: Optional[str] = None
    password: str