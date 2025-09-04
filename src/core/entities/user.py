from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from .user_role import UserRole

class User(BaseModel):

    name: constr(strip_whitespace=True, min_length=4)
    email: EmailStr
    password_hash: str
    role: UserRole
    id: Optional[int] = None

class Config:
    from_attributes = True