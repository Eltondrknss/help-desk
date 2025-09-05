from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Annotated
from .user_role import UserRole

class User(BaseModel):

    name: Annotated[str, StringConstraints(strip_whitespace=True, min_length=4)]
    email: EmailStr
    password_hash: str
    role: UserRole
    id: Optional[int] = None

class Config:
    from_attributes = True