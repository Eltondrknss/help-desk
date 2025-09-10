from datetime import datetime
from typing import Optional
from src.core.entities.user import User
from src.core.entities.ticket import Ticket
from src.core.entities.user_role import UserRole
from src.core.entities.ticket_status import TicketStatus
from src.core.repositories.ticket_repository import ITicketRepository
from src.core.exceptions import PermissionDeniedError, ResourceNotFoundError, InvalidStateError, ValidationError

class UpdateTicketStatus:

    def __init__(self, ticket_repository: ITicketRepository):
        self.ticket_repository = ticket_repository

    def execute(self, requester: User, ticket_id: int, new_status: TicketStatus, justification: Optional[str] = None) -> Ticket:
        #verifica a permissao do usuario
        if requester.role not in [UserRole.TECHNICIAN, UserRole.ADMIN]:
            raise PermissionDeniedError("Apenas técnicos e admins podem atualizar chamados.")
    
        #busca o chamado
        ticket = self.ticket_repository.find_by_id(ticket_id)
        if not ticket:
            raise ResourceNotFoundError(f"Nenhum chamado com o ID {ticket_id}.")
        
        #regras de negocio
        if ticket.status == TicketStatus.CLOSED:
            raise InvalidStateError("Não é possivel alterar um chamado que ja está fechado.")
        
        #regra para nao permitir fechar chamado sem inserir justificativa
        if new_status == TicketStatus.CLOSED and (not justification or not justification.strip()):
            raise ValidationError("É necessário inserir uma justificativa para fechar um chamado.")
        
        #ao alterar o status, caso nao tenha tecnico, vincula o logado.
        if new_status in [TicketStatus.IN_PROGRESS, TicketStatus.CLOSED] and not ticket.technician_id:
            ticket.technician_id = requester.id

        ticket.status = new_status
        if new_status == TicketStatus.CLOSED:
            ticket.closing_justification = justification
        ticket.updated_at = datetime.now()

        updated_ticket = self.ticket_repository.update(ticket)
        return updated_ticket