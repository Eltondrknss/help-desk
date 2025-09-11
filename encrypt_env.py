from cryptography.fernet import Fernet

#Lê a chave do arquivo secret.key
try:
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()
except FileNotFoundError:
    print("❌ ERRO: Arquivo 'secret.key' não encontrado.")
    print("    Execute 'python generate_key.py' primeiro para criar a chave.")
    exit(1)

fernet = Fernet(key)

#Lê o conteúdo do arquivo .env
try:
    with open('.env', 'rb') as file:
        original_content = file.read()
except FileNotFoundError:
    print("❌ ERRO: Arquivo '.env' não encontrado para criptografar.")
    exit(1)


#Criptografa o conteúdo
encrypted_content = fernet.encrypt(original_content)

#Escreve o conteúdo criptografado
with open('.env.encrypted', 'wb') as encrypted_file:
    encrypted_file.write(encrypted_content)

print("✅ Arquivo .env criptografado com sucesso como .env.encrypted")