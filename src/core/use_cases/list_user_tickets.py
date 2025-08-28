from typing import List
from src.core.entities.ticket import Ticket
from src.core.repositories.ticket_repository import ITicketRepository

class ListUserTickets:
    #lista todos os chamados do usuário logado

    def __init__(self, ticket_repository: ITicketRepository):
        self.ticket_repository = ticket_repository

    def execute(self, user_id: int) -> List[Ticket]:
        user_tickets = self.ticket_repository.find_by_user_id(user_id)
        return user_tickets