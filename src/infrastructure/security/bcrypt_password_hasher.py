import bcrypt
from src.core.security.password_hasher import IPasswordHasher

class BcryptPasswordHasher(IPasswordHasher):
    
    def hash(self, password: str) -> str:
        password_bytes = password.encode('utf-8')

        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(password_bytes, salt)

        return hashed_bytes.decode('utf-8')
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        plain_password_bytes = plain_password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')

        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)