from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .ticket_status import TicketStatus

@dataclass
class Ticket:

    title: str
    description: str
    status: TicketStatus
    user_id: int

    id: Optional[int] = None
    technician_id: Optional[int] = None

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)