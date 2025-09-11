import os
import io
from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken

def load_decrypted_dotenv():

    try:

        project_root = Path(__file__).parent.parent
        key_path = project_root / 'secret.key'
        encrypted_env_path = project_root / '.env.encrypted'
        
        with open(key_path, 'rb') as key_file:
            key = key_file.read()

    except FileNotFoundError:
        print("ERRO CRÍTICO: Arquivo de chave 'secret.key' não encontrado na raiz do projeto.")
        print("              Execute 'python generate_key.py' para criá-lo.")
        exit(1)

    try:
        fernet = Fernet(key)
        
        with open(encrypted_env_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)
        
        string_io = io.StringIO(decrypted_data.decode())
        load_dotenv(stream=string_io)
        
    except FileNotFoundError:
        print("ERRO CRÍTICO: Arquivo de configurações '.env.encrypted' não encontrado.")
        print("              Execute 'python encrypt_env.py' para criá-lo.")
        exit(1)
    except InvalidToken:
        print("ERRO CRÍTICO: A chave em 'secret.key' não corresponde ao arquivo '.env.encrypted'.")
        print("              Execute 'python encrypt_env.py' novamente para sincronizar.")
        exit(1)
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar configurações: {e}")
        exit(1)

load_decrypted_dotenv()

class Settings:

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")

settings = Settings()