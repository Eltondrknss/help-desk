from src.core.use_cases.create_user import CreateUser
from src.core.use_cases.list_users import ListUsers
from src.core.use_cases.login_user import LoginUser, InvalidCredentialsError
from src.core.entities.user import User
from src.core.entities.user_role import UserRole
from src.presentation.cli.cli_utils import non_empty_input
from src.core.exceptions import ApplicationError, ResourceNotFoundError, AuthenticationError, PermissionDeniedError
from pydantic import ValidationError


class UserCLI:
    
    def __init__(self, create_user_case: CreateUser, list_users_case: ListUsers, login_user_case: LoginUser):
        self.create_user_case = create_user_case
        self.list_users_case = list_users_case
        self.login_user_case = login_user_case


    def create_user_flow(self):
        
        print("\n--- Cadastro de Novo Usuário ---")

        try:
            name = non_empty_input("Nome: ")
            email = non_empty_input("E-mail: ")
            password = non_empty_input("Senha: ")

            print("Escolha o cargo: 1-Admin, 2-Tecnico, 3-Usuario")
            role_choice = non_empty_input("> ")
            role_map = {
                "1": UserRole.ADMIN,
                "2": UserRole.TECHNICIAN,
                "3": UserRole.USER
            }
            role = role_map.get(role_choice, UserRole.USER)

            created_user = self.create_user_case.execute(
                name=name,
                email=email,
                password=password,
                role=role
            )
            print("\n✅ Usuário criado com sucesso!")
            print(f"ID: {created_user.id}, Nome: {created_user.name}. Email: {created_user.email}, Cargo: {created_user.role.value}")

        except ValidationError as e:
            # Captura erros de negócio (ex: email duplicado) e mostra ao usuário
            print(f"\n❌ Erro de validação. Por favor corrija os seguinte campos:")
            for error in e.errors():
                campo = error['loc'][0]
                mensagem = error['msg']
                print(f" - Campo '{campo}': {mensagem}")
        
        except ApplicationError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            # Captura outros erros inesperados
            print(f"\n❌ Ocorreu um erro inesperado: {e}")

    def list_users_flow(self, logged_in_user: User):
        print("\n--- Lista de usuários cadastrados ---")
        try:
            users = self.list_users_case.execute(requester=logged_in_user)
            if not users:
                print("Nenhum usu[ario encontrado.")
                return
            
            for user in users:
                print(f"ID: {user.id} | Nome: {user.name} | Email: {user.email} | Cargo: {user.role.value}")

        except PermissionDeniedError as e:
            print(f"\n❌ Acesso Negado: {e}")

        except Exception as e:
            print(f"\n❌ Ocorreu um erro ao listar os usuários: {e}")

    def login_flow(self):
        print("\n--- Login ---")
        try:
            email = non_empty_input("Email: ")
            password = non_empty_input("Senha: ")

            logged_in_user = self.login_user_case.execute(email = email, password = password)
            
            print(f"\n✅ Logado com sucesso! Bem vindo {logged_in_user.name}!")

            return logged_in_user

        except (ResourceNotFoundError, AuthenticationError) as e:
            print(f"\n❌ Falha no login: email ou senha inválidos")
            return None
        except Exception as e:
            print(f"\n❌ Ocorreu um erro inesperado: {e}")
            return None