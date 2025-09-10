from pydantic import BaseModel, Field, StringConstraints
from datetime import datetime
from typing import Optional, Annotated
from .ticket_status import TicketStatus

class Ticket(BaseModel):
    
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10)]
    description: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10)]
    status: TicketStatus
    user_id: int

    id: Optional[int] = None
    technician_id: Optional[int] = None

    closing_justification: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Config:
    from_attributes = True