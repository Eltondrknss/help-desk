from src.infrastructure.database.mysql_user_repository import MySQLUserRepository
from src.infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher

from src.core.use_cases.create_user import CreateUser
from src.core.use_cases.list_users import ListUsers
from src.core.use_cases.login_user import LoginUser

from src.presentation.cli.user_cli import UserCLI

def main():

    print("Iniciando o Sistema de Chamados...")

    password_hasher = BcryptPasswordHasher()
    user_repository = MySQLUserRepository()

    create_user_case = CreateUser(user_repository=user_repository, password_hasher=password_hasher)
    list_users_case = ListUsers(user_repository=user_repository)
    login_user_case = LoginUser(user_repository=user_repository, password_hasher=password_hasher)

    user_cli = UserCLI(create_user_case=create_user_case, list_users_case=list_users_case, login_user_case=login_user_case)


    while True:
        print("\n--- Menu Principal ---")
        print("1. Login")
        print("2. Criar Novo Usuário")
        print("3. Listar Usuários")
        print("4. Sair")
        choice = input("> ")

        if choice == "1":
            user_cli.login_flow()
        elif choice == "2":
            user_cli.create_user_flow()
        elif choice == "3":
            user_cli.list_users_flow()
        elif choice == "4":
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente")

if __name__ == "__main__":
    main()