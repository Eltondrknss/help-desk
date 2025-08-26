from src.core.entities.user import User
from src.core.entities.user_role import UserRole
from src.core.repositories.user_repository import IUserRepository
from src.core.security.password_hasher import IPasswordHasher

class CreateUser:

    def __init__(
            self,
            user_repository: IUserRepository,
            password_hasher: IPasswordHasher
    ):
        
        self.user_repository = user_repository
        self.password_hasher = password_hasher
    
    def execute(self, name:str, email: str, password: str, role: UserRole) -> User:
        existing_user = self.user_repository.find_by_email(email)
        if existing_user:
            raise ValueError(f"O email '{email}' já está em uso.")
        
        password_hash = self.password_hasher.hash(password)

        new_user = User(
            name = name,
            email = email,
            password_hash = password_hash,
            role = role
        )

        created_user = self.user_repository.save(new_user)

        return created_user