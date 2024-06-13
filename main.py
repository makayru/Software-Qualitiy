from encryption import RSAEncryption
from user_manager import UserManager
from getpass import getpass

class Application:
    def __init__(self):
        self.encryption = RSAEncryption()
        self.user_manager = UserManager(self.encryption)

    def run(self):
        while True:
            print("\n1. Register\n2. Log In\n3. Exit")
            choice = input("Choose an option: ")
            
            if choice == '1':
                username = input("Enter username: ")
                password = getpass("Enter password: ")
                role = input("Enter role (super_admin/system_admin/consultant): ")
                self.user_manager.register_user(username, password, role)
            
            elif choice == '2':
                username = input("Enter username: ")
                password = getpass("Enter password: ")
                self.user_manager.authenticate_user(username, password)
            
            elif choice == '3':
                self.user_manager.close()
                break
            
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = Application()
    app.run()
