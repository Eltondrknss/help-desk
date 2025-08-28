from typing import List
from src.core.entities.user import User
from src.core.entities.user_role import UserRole
from src.core.repositories.user_repository import IUserRepository

class ListUsers:

    def __init__ (self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self, requester: User) -> List[User]:
        if requester.role != UserRole.ADMIN:
            raise PermissionError("Apenas administradores podem listar todos os usuários")
        
        users = self.user_repository.find_all()
        return users