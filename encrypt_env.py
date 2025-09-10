import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()
key_str = os.getenv("DOTENV_KEY")

if not key_str:
    raise ValueError("Chave de criptografia não encontrada na variavel de ambiente DOTENV_KEY")

key = key_str.encode()
fernet = Fernet(key)

with open('.env', 'rb') as file:
    original_content = file.read()

encrypted_content = fernet.encrypt(original_content)

with open ('/env.encrypted', 'wb') as encrypted_file:
    encrypted_file.write(encrypted_content)


print("✅ Arquivo .env criptografado com sucesso como .env.encrypted")
print("🔒 Lembre-se de apagar ou proteger o arquivo .env original.")