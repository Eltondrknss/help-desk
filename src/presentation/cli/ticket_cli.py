from src.core.entities.user import User
from src.core.entities.ticket_status import TicketStatus
from src.core.use_cases.create_ticket import CreateTicket
from src.core.use_cases.list_user_tickets import ListUserTickets
from src.core.use_cases.list_open_tickets import ListOpenTickets
from src.core.use_cases.update_ticket_status import UpdateTicketStatus
from src.presentation.cli.cli_utils import non_empty_input
from src.core.exceptions import ValidationError, PermissionDeniedError

class TicketCLI:
    
    def __init__(
            self,
            create_ticket_case: CreateTicket,
            list_user_tickets_case: ListUserTickets,
            list_open_tickets_case: ListOpenTickets,
            update_ticket_status_case: UpdateTicketStatus
    ):
        self.create_ticket_case = create_ticket_case
        self.list_user_tickets_case = list_user_tickets_case
        self.list_open_tickets_case = list_open_tickets_case
        self.update_ticket_status_case = update_ticket_status_case

    def create_ticket_flow(self, logged_in_user: User):

        if not logged_in_user:
            print("\n❌ Você precisa estar logado para criar um chamado.")
            return
        
        print("\n--- Abertura de Novo Chamado ---")
        try:
            title = non_empty_input("Titulo: ")
            description = non_empty_input("Descrição detalhada do problema: ")
            created_ticket = self.create_ticket_case.execute(title=title, description=description, user_id= logged_in_user.id)

            print("\n✅ Chamado criado com sucesso!")
            print(f"ID: {created_ticket.id}, Titulo: {created_ticket.title}, Status: {created_ticket.status.value}")

        except ValidationError as e:
            print(f"\n❌ Erro ao criar chamado: {e}")
        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado: {e}")

    def list_my_tickets_flow(self, logged_in_user: User):
        if not logged_in_user:
            print("\n❌ Voce precisa estar logado para ver seus chamados.") 
            return
        
        print(f"\n--- Meus chamados (Usuário: {logged_in_user.name}) ---")
        try:
            my_tickets = self.list_user_tickets_case.execute(user_id=logged_in_user.id)

            if not my_tickets:
                print("Voce ainda não abriu nenhum chamado.")
                return
            
            for ticket in my_tickets:
                print(f"  ID: {ticket.id} | Status: {ticket.status.value.upper()} | Título: {ticket.title}")
                print(f"    Criado em: {ticket.created_at.strftime('%d/%m/%Y %H:%M')}")

        except ValidationError as e:
            print(f"\n❌ Ocorreu um erro ao buscar seus chamados: {e}")

    def technician_update_flow(self, logged_in_user: User):
        
        print("\n--- Fila de chamados Abertos ---")
        try:
            open_tickets = self.list_open_tickets_case.execute(requester=logged_in_user)
            if not open_tickets:
                print("Não existem chamados abertos no momento.")
                return
            
            for ticket in open_tickets:
                print(f"  ID: {ticket.id} | Status: {ticket.status.value.upper()} | Título: {ticket.title}")

            ticket_id_str = non_empty_input("\nDigite o ID do chamado que quer atualizar (ou 'c' para cancelar):")
            if ticket_id_str.lower() == 'c':
                return
            
            ticket_id = int(ticket_id_str)

            print("Escolha o novo status: 1- Em andamento, 2- Fechado")
            status_choice = non_empty_input("> ")
            status_map = {
                "1": TicketStatus.IN_PROGRESS,
                "2": TicketStatus.CLOSED
            }
            new_status = status_map.get(status_choice)
            if not new_status:
                print("Opção inválida.")
                return
            
            updated_ticket = self.update_ticket_status_case.execute(
                requester=logged_in_user,
                ticket_id=ticket_id,
                new_status=new_status
            )

            print("\n✅ Chamado atualizado com sucesso!")
            print(f"  ID: {updated_ticket.id} | Novo Status: {updated_ticket.status.value.upper()} | Técnico: {updated_ticket.technician_id}")

        except (ValidationError, PermissionDeniedError) as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado: {e}")