from src.core.entities.ticket import Ticket
from src.core.entities.ticket_status import TicketStatus
from src.core.repositories.ticket_repository import ITicketRepository
from src.core.exceptions import ValidationError

class CreateTicket:

    def __init__(self, ticket_repository: ITicketRepository):
        self.ticket_repository = ticket_repository

    def execute(self, title: str, description: str, user_id: int) -> Ticket:
        
        if not title:
            raise ValidationError("O titulo do chamado não pode ser vazio.")
        
        new_ticket = Ticket(
            title=title,
            description=description,
            user_id=user_id,
            status=TicketStatus.OPEN
        )

        created_ticket = self.ticket_repository.save(new_ticket)

        return created_ticket