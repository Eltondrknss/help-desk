from typing import List, Optional
from src.core.entities.ticket import Ticket
from src.core.entities.ticket_status import TicketStatus
from src.core.repositories.ticket_repository import ITicketRepository
from .db_connection_handler import db_handler

class MySQLTicketRepository(ITicketRepository):
    def __init__(self):
        self.table_name = "tickets"

    def _row_to_entity(self, row: dict) -> Ticket:
        #Metodo auxiliar para converter uma linha do banco em uma entidade Ticket
        #O banco retorna o status como string, entao convertemos de volta para Enum
        row['status'] = TicketStatus(row['status'])
        return Ticket(**row)
    
    def save(self, ticket: Ticket) -> Ticket:
        query = f"""
            INSERT INTO {self.table_name}
            (title, description, status, user_id, technician_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            ticket.title, ticket.description, ticket.status.value,
            ticket.user_id, ticket.technician_id,
            ticket.created_at, ticket.updated_at
        )
        with db_handler.managed_cursor() as cursor:
            cursor.execute(query, params)
            ticket.id = cursor.lastrowid
        return ticket
    
    def find_by_id(self, ticket_id: int) -> Optional[Ticket]:
        query = f"SELECT * FROM {self.table_name} WHERE id = %s"
        with db_handler.managed_cursor() as cursor:
            cursor.execute(query, (ticket_id,))
            row = cursor.fetchone()
        return self._row_to_entity(row) if row else None
    
    def find_all(self) -> List[Ticket]:
        query = f"SELECT * FROM {self.table_name}"
        tickets: List[Ticket] = []
        with db_handler.managed_cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            tickets.append(self._row_to_entity(row))
        return tickets
    
    def find_by_user_id(self, user_id: int) -> List[Ticket]:
        query = f"SELECT * FROM {self.table_name} WHERE user_id = %s"
        tickets: List[Ticket] = []
        with db_handler.managed_cursor() as cursor:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

        for row in rows:
            tickets.append(self._row_to_entity(row))
        return tickets