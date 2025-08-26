from typing import List, Optional
from src.core.entities.user import User
from src.core.entities.user_role import UserRole
from src.core.repositories.user_repository import IUserRepository
from .db_connection_handler import db_handler

class MySQLUserRepository(IUserRepository):

    def __init__(self):
        self.table_name = "users"

    def save(self, user: User) -> User:
        query = f"""
            INSERT INTO {self.table_name} (name, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
        """
        params = (user.name, user.email, user.password_hash, user.role.value)

        with db_handler.managed_cursor() as cursor:
            cursor.execute(query, params)
            user.id = cursor.lastrowid
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        query = f"SELECT id, name, email, password_hash, role FROM {self.table_name} WHERE id = %s"

        with db_handler.managed_cursor() as cursor:
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()

        if row:
            row['role'] = UserRole(row['role'])
            return User(**row)
        return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        query = f"SELECT id, name, email, password_hash, role FROM {self.table_name} WHERE email = %s"

        with db_handler.managed_cursor() as cursor:
            cursor.execute(query, (email,))
            row = cursor.fetchone()

        if row:
            row['role'] = UserRole(row['role'])
            return User(**row)
        return None
    
    def find_all(self) -> List[User]:
        query = f"SELECT id, name, email, password_hash, role FROM {self.table_name}"

        users: List[User] = []

        with db_handler.managed_cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            row['role'] = UserRole(row['role'])
            users.append(User(**row))

        return users