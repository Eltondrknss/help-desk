import os
import io
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken

def load_decrypted_dotenv():

    key_str = os.getenv("DOTENV_KEY")
    if not key_str:
        print(f"AVISO: chave de criptografia não encontrada. Tentando carregar .env normal.")
        load_dotenv()
        return
    
    try:
        key = key_str.encode()
        fernet = Fernet(key)

        with open('.env.encrypted', 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        string_io = io.StringIO(decrypted_data.decode())
        load_dotenv(stream=string_io)

    except FileNotFoundError:
        print("AVISO: Arquivo .env.encrypted não encontrado. A aplicação pode não funcionar corretamente.")
    except InvalidToken:
        print("ERRO CRÍTICO: A chave de criptografia (DOTENV_KEY) é inválida ou não corresponde. Não foi possível descriptografar as configurações.")
        exit(1) # Encerra a aplicação se a chave for errada
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar configurações: {e}")
        exit(1)
        

class Settings:
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")

settings = Settings()