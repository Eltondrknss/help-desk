from src.core.entities.user import User
from src.core.repositories.user_repository import IUserRepository
from src.core.security.password_hasher import IPasswordHasher
from src.core.exceptions import AuthenticationError

class InvalidCredentialsError(Exception):
    pass

class LoginUser:

    def __init__(self, user_repository: IUserRepository, password_hasher: IPasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, email: str, password: str) -> User:

        user = self.user_repository.find_by_email(email)
        if not user:
            raise AuthenticationError("Email ou senha inválidos.")
        
        is_password_valid = self.password_hasher.verify(plain_password = password, hashed_password = user.password_hash)

        if not is_password_valid:
            raise AuthenticationError("Email ou senha inválidos.")
        
        return user