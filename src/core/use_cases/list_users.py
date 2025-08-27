from typing import List
from src.core.entities.user import User
from src.core.repositories.user_repository import IUserRepository

class ListUsers:

    def __init__ (self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def execute(self) -> List[User]:
        users = self.user_repository.find_all()
        return users