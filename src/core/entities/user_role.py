from enum import Enum

class UserRole(Enum):
    "Define os cargos disponíveis para serem usados no sistema"

    ADMIN = "admin"
    TECHNICIAN = "tecnico"
    USER = "usuario"
    