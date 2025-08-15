import mysql.connector
from contextlib import contextmanager
from src.config import settings

class DBConnectionHandler:

    def __init__(self):
        self._connection_config = {
            "host": settings.DB_HOST,
            "port": settings.DB_PORT,
            "user": settings.DB_USER,
            "password": settings.DB_PASSWORD,
            "database": settings.DB_NAME,
        }
        self.connection = None
        self.cursor = None

    @contextmanager
    def managed_cursor(self):
        try:
            self.connection = mysql.connector.connect(**self._connection_config)
            self.cursor = self.connection.cursor(dictionary=True)
            yield self.cursor
            self.connection.commit()
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            print(f"Erro no banco de dados: {e}")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection and self.connection.is_connected():
                self.connection.close()

db_handler = DBConnectionHandler()