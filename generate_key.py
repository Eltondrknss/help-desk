from cryptography.fernet import Fernet

key = Fernet.generate_key()

print("Guarde essa chave em um lugar seguro!!!!!")
print(key.decode())