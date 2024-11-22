import json
import os
from .manager_services import DataManager

class UserDataManager:
    def __init__(self, file_path="src/dataset/user_data.json"):
        self.file_path = file_path
        self.encrypt = DataManager()

    def save_user_data(self, username, password, subdomain):

        encrypted = self.encrypt.encrypt_data(password)

        print(encrypted)

        data = {
            "username": username,
            "password": encrypted,
            "subdomain": subdomain
        }
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def load_user_data(self):
        if not os.path.exists(self.file_path):
            return None
        with open(self.file_path, "r") as file:
            data = json.load(file)
        if data and "password" in data:
            data["password"] = self.encrypt.decrypt_data(data["password"])
        return data

    def clear_user_data(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

if __name__ == "__main__":
    user_manager = UserDataManager()

    user_manager.save_user_data("test_user", "secure_password", "test_subdomain")

    user_data = user_manager.load_user_data()
    print("Loaded data:", user_data)

    user_manager.clear_user_data()
    print("Data cleared. File exists:", os.path.exists("src/dataset/user_data.json"))
