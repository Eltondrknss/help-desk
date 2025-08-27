from src.core.entities.user import User
from src.core.use_cases.create_ticket import CreateTicket

class TicketCLI:
    
    def __init__(self, create_ticket_case: CreateTicket):
        self.create_ticket_case = create_ticket_case

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