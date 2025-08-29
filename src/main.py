#infraestrutura
from src.infrastructure.database.mysql_user_repository import MySQLUserRepository
from src.infrastructure.database.mysql_ticket_repository import MySQLTicketRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

#core
from src.core.entities.user_role import UserRole
from src.core.use_cases.create_user import CreateUser
from src.core.use_cases.list_users import ListUsers
from src.core.use_cases.login_user import LoginUser
from src.core.use_cases.create_ticket import CreateTicket
from src.core.use_cases.list_user_tickets import ListUserTickets
from src.core.use_cases.list_open_tickets import ListOpenTickets
from src.core.use_cases.update_ticket_status import UpdateTicketStatus

#apresentacao
from src.presentation.cli.user_cli import UserCLI
from src.presentation.cli.ticket_cli import TicketCLI

def main():

    print("Iniciando o Sistema de Chamados...")

    #container de injecao de dependencia

    #repositorios
    password_hasher = BcryptPasswordHasher()
    user_repository = MySQLUserRepository()
    ticket_repository = MySQLTicketRepository()

    #casos de uso
    create_user_case = CreateUser(user_repository=user_repository, password_hasher=password_hasher)
    list_users_case = ListUsers(user_repository=user_repository)
    login_user_case = LoginUser(user_repository=user_repository, password_hasher=password_hasher)
    create_ticket_case = CreateTicket(ticket_repository=ticket_repository)
    list_user_tickets_case = ListUserTickets(ticket_repository=ticket_repository)
    list_open_tickets_case = ListOpenTickets(ticket_repository=ticket_repository)
    update_ticket_status_case = UpdateTicketStatus(ticket_repository=ticket_repository)

    #CLI
    user_cli = UserCLI(
        create_user_case=create_user_case,
        list_users_case=list_users_case,
        login_user_case=login_user_case
        )
    ticket_cli = TicketCLI(
        create_ticket_case=create_ticket_case,
        list_user_tickets_case=list_user_tickets_case,
        list_open_tickets_case=list_open_tickets_case,
        update_ticket_status_case=update_ticket_status_case
        )

    #gerenciamento de sessao
    logged_in_user = None

    while True:
        if logged_in_user:
            #menu para usuarios logados
            print(f"\n--- Menu Principal (Logado como: {logged_in_user.name} [{logged_in_user.role.value}]) ---")
            print("1. Abrir Novo Chamado")
            print("2. Meus Chamados")

            if logged_in_user.role in [UserRole.TECHNICIAN, UserRole.ADMIN]:
                print("3. Fila de chamados para atender")

            if logged_in_user.role == UserRole.ADMIN:
                print("4. Listar todos os usuários")
            
            print("0. Logout")
            choice = input("> ")

            if choice == "1":
                ticket_cli.create_ticket_flow(logged_in_user)
            elif choice == "2":
                ticket_cli.list_my_tickets_flow(logged_in_user)
            elif choice == "3":
                ticket_cli.technician_update_flow(logged_in_user)
            elif choice == "4" and logged_in_user.role == UserRole.ADMIN:
                user_cli.list_users_flow(logged_in_user)
            elif choice == "0":
                logged_in_user = None
                print("\nUsuário deslogado com sucesso!")
            else:
                print("Opção inválida. Tente novamente")

        else:
            #menu para usuarios deslogados
            print("\n--- Menu Principal (Visitante) ---")
            print("1. Login")
            print("2. Criar Novo Usuário")
            print("0. Sair")
            choice = input("> ")

            if choice == "1":
                logged_in_user = user_cli.login_flow()
            elif choice == "2":
                user_cli.create_user_flow()
            elif choice == "0":
                print("Fechando sistema. Até logo!")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    main()