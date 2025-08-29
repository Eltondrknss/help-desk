from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities.ticket import Ticket
from src.core.entities.ticket_status import TicketStatus

class ITicketRepository(ABC):

    @abstractmethod
    def save(self, ticket: Ticket) -> Ticket:
        pass

    @abstractmethod
    def find_by_id(self, ticket_id: int) -> Optional[Ticket]:
        pass

    @abstractmethod
    def find_all(self) -> List[Ticket]:
        pass

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Ticket]:
        pass

    @abstractmethod
    def update(self, ticket: Ticket) -> Ticket:
        pass

    @abstractmethod
    def find_by_status(self, status: TicketStatus) -> List[Ticket]:
        pass

    @abstractmethod
    def find_unclosed(self) -> List[Ticket]:
        pass