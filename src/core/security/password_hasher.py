from abc import ABC, abstractmethod

class IPasswordHasher(ABC):

    @abstractmethod
    def hash(self, password: str) -> str:
        # Gera o hash de uma senha em texto e retorna o hash como string
        pass

    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        # verifica se tem um hash existente com a mesma senha em texto 
        pass

