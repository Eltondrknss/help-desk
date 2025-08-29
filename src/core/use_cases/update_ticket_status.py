from datetime import datetime
from src.core.entities.user import User
from src.core.entities.ticket import Ticket
from src.core.entities.user_role import UserRole
from src.core.entities.ticket_status import TicketStatus
from src.core.repositories.ticket_repository import ITicketRepository

class UpdateTicketStatus:

    def __init__(self, ticket_repository: ITicketRepository):
        self.ticket_repository = ticket_repository

    def execute(self, requester: User, ticket_id: int, new_status: TicketStatus) -> Ticket:
        #verifica a permissao do usuario
        if requester.role not in [UserRole.TECHNICIAN, UserRole.ADMIN]:
            raise PermissionError("Apenas técnicos e admins podem atualizar chamados.")
    
        #busca o chamado
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Nenhum chamado com o ID {ticket_id}.")
        
        #regras de negocio
        if ticket.status == TicketStatus.CLOSED:
            raise ValueError("Não é possivel alterar um chamado que ja está fechado.")
        
        #ao alterar o status, caso nao tenha tecnico, vincula o logado.
        if new_status in [TicketStatus.IN_PROGRESS, TicketStatus.CLOSED] and not ticket.technician_id:
            ticket.technician_id = requester.id

        ticket.status = new_status
        ticket.updated_at = datetime.now()

        updated_ticket = self.ticket_repository.update(ticket)
        return updated_ticket