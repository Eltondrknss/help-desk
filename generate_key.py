from cryptography.fernet import Fernet

key = Fernet.generate_key()

try:
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
        print(key)
    print("✅ Chave de criptografia gerada e salva no arquivo 'secret.key'.")
    print("🔑 Garanta que ele esteja no seu .gitignore.")
except IOError as e:
    print(f"❌ Erro ao escrever o arquivo de chave: {e}")