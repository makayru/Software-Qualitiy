# main.py
from user_manager import UserManager
from member_manager import MemberManager
from getpass import getpass
from menus import main_menu
from menu_handler import MenuHandler
from logger import LoggerDatabaseManager

class Application:
    def __init__(self):
        self.logger = LoggerDatabaseManager()
        self.user_manager = UserManager(self.logger)
        self.member_manager = MemberManager(self.logger)
        self.menu_handler = MenuHandler(self.user_manager, self.member_manager)

    def run(self):
        while True:
            option = main_menu()
            if option == '1':
                username = input("Enter username: ")
                password = getpass("Enter password: ")
                role = self.user_manager.authenticate_user(username, password)
                if role:
                    self.menu_handler.display_role_based_menu(role)
            elif option == '2':
                self.user_manager.close()
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = Application()
    app.run()
