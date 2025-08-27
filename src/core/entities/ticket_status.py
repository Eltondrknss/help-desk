from enum import Enum

class TicketStatus(Enum):

    OPEN = "aberto"
    IN_PROGRESS = "em_atendimento"
    CLOSED = "fechado"