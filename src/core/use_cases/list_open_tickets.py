from typing import List
from src.core.entities.user import User
from src.core.entities.ticket import Ticket
from src.core.entities.user_role import UserRole
from src.core.repositories.ticket_repository import ITicketRepository

class ListOpenTickets:

    def __init__(self, ticket_repository: ITicketRepository):
        self.ticket_repository = ticket_repository

    def execute(self, requester: User) -> List[Ticket]:
        if requester.role not in [UserRole.TECHNICIAN, UserRole.ADMIN]:
            raise PermissionError("Apenas técnicos e administradores podem listar todos os chamados abertos.")
        
        open_tickets = self.ticket_repository.find_unclosed()
        return open_tickets