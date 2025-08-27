#infraestrutura
from src.infrastructure.database.mysql_user_repository import MySQLUserRepository
from src.infrastructure.database.mysql_ticket_repository import MySQLTicketRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

#core
from src.core.use_cases.create_user import CreateUser
from src.core.use_cases.list_users import ListUsers
from src.core.use_cases.login_user import LoginUser
from src.core.use_cases.create_ticket import CreateTicket

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

    #CLI
    user_cli = UserCLI(create_user_case=create_user_case, list_users_case=list_users_case, login_user_case=login_user_case)
    ticket_cli = TicketCLI(create_ticket_case=create_ticket_case)

    #gerenciamento de sessao
    logged_in_user = None

    while True:
        if logged_in_user:
            #menu para usuarios logados
            print(f"\n--- Menu Principal (Logado como: {logged_in_user.name}) ---")
            print("1. Abrir Novo Chamado")
            print("2. Meus Chamados")
            print("3. Logout")
            choice = input("> ")

            if choice == "1":
                ticket_cli.create_ticket_flow(logged_in_user)
            elif choice == "3":
                logged_in_user = None
                print("\nUsuário deslogado com sucesso!")
            else:
                print("Opção inválida. Tente novamente")

        else:
            #menu para usuarios deslogados
            print("\n--- Menu Principal (Visitante) ---")
            print("1. Login")
            print("2. Criar Novo Usuário")
            print("3. Listar todos os Usuários")
            print("4. Sair")
            choice = input("> ")

            if choice == "1":
                logged_in_user = user_cli.login_flow()
            elif choice == "2":
                user_cli.create_user_flow()
            elif choice == "3":
                user_cli.list_users_flow()
            elif choice == "4":
                print("Fechando sistema. Até logo!")
                break
            else:
                print("Opção inválida.")

def patch_user_cli_login():
    from src.presentation.cli.user_cli import UserCLI
    original_login_flow = UserCLI.login_flow

    def patched_login_flow(self):
        logged_in_user = original_login_flow(self)
        return logged_in_user
    
    UserCLI.login_flow = patched_login_flow
    
if __name__ == "__main__":

    def new_login_flow(self):
        print("\n--- Login ---")
        try:
             email = input("Email: ")
             password = input("Senha: ")
             logged_in_user = self.login_user_case.execute(email=email, password=password)
             print(f"\n✅ Logado com sucesso! Bem vindo, {logged_in_user.name}!")
             return logged_in_user
        except Exception as e:
            print(f"\n❌ Falha no login: {e}")
            return None
        
    UserCLI.login_flow = new_login_flow

    main()