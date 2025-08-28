from src.core.entities.user import User
from src.core.use_cases.create_ticket import CreateTicket
from src.core.use_cases.list_user_tickets import ListUserTickets

class TicketCLI:
    
    def __init__(self, create_ticket_case: CreateTicket, list_user_tickets_case: ListUserTickets):
        self.create_ticket_case = create_ticket_case
        self.list_user_tickets_case = list_user_tickets_case

    def create_ticket_flow(self, logged_in_user: User):

        if not logged_in_user:
            print("\n❌ Você precisa estar logado para criar um chamado.")
            return
        
        print("\n--- Abertura de Novo Chamado ---")
        try:
            title = input("Titulo: ")
            description = input("Descrição detalhada do problema: ")
            created_ticket = self.create_ticket_case.execute(title=title, description=description, user_id= logged_in_user.id)

            print("\n✅ Chamado criado com sucesso!")
            print(f"ID: {created_ticket.id}, Titulo: {created_ticket.title}, Status: {created_ticket.status.value}")

        except ValueError as e:
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

        except Exception as e:
            print(f"\n❌ Ocorreu um erro ao buscar seus chamados: {e}")