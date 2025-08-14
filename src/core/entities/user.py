from dataclasses import dataclass
from typing import Optional
from .user_role import UserRole

@dataclass
class USUARIO:
    nome: str
    email: str
    password_hash: str
    role: UserRole
    id: Optional[int] = None