from cryptography.fernet import Fernet
import base64
import os

class DataManager:
    def __init__(self, key_file="src/dataset/secret.key"):
        if os.path.exists(key_file):
            with open(key_file, "rb") as keyfile:
                self.key = keyfile.read()
            try:
                base64.urlsafe_b64decode(self.key)
            except Exception as e:
                raise ValueError("Invalid key format in file.") from e
        else:
            self.key = Fernet.generate_key()
            with open(key_file, "wb") as keyfile:
                keyfile.write(self.key) 
        self.cipher = Fernet(self.key)

    def encrypt_data(self, password):
        encrypted_data = self.cipher.encrypt(password.encode())
        encrypted_string = base64.urlsafe_b64encode(encrypted_data).decode()
        return encrypted_string

    def decrypt_data(self, encrypted_string):
        encrypted_data = base64.urlsafe_b64decode(encrypted_string.encode())
        decrypted_password = self.cipher.decrypt(encrypted_data).decode()
        return decrypted_password

if __name__ == "__main__":
    data_manager = DataManager()

    user_data = {
        "username": "test_user",
        "password": "secure_password",
        "subdomain": "test_subdomain"
    }

    encrypted_data = data_manager.encrypt_data(user_data)
    print("Зашифрованные данные:", encrypted_data)

    decrypted_data = data_manager.decrypt_data(encrypted_data)
    print("Расшифрованные данные:", decrypted_data)
