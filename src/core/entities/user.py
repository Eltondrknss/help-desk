from dataclasses import dataclass
from typing import Optional
from .user_role import UserRole

@dataclass
class User:
    name: str
    email: str
    password_hash: str
    role: UserRole
    id: Optional[int] = None