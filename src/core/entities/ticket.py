from pydantic import BaseModel, Field, constr
from datetime import datetime
from typing import Optional
from .ticket_status import TicketStatus

class Ticket(BaseModel):
    
    title: constr(strip_whitespace=True, min_length=5)
    description: constr(strip_whitespace=True, min_length=1)
    status: TicketStatus
    user_id: int

    id: Optional[int] = None
    technician_id: Optional[int] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Config:
    from_attributes = True