# main.py
from user_manager import UserManager
from member_manager import MemberManager
from consultant_manager import ConsultantManager
from systemadmin_manager import SystemAdminManager
from superadmin_manager import SuperAdminManager
from getpass import getpass
from menus import main_menu
from menu_handler import MenuHandler
from logger import LoggerDatabaseManager
import time

class Application:
    def __init__(self):
        self.logger = LoggerDatabaseManager()
        self.user_manager = UserManager(self.logger)
        self.member_manager = MemberManager(self.logger)
        self.consultant_manager = ConsultantManager(self.logger)
        self.systemadmin_manager = SystemAdminManager(self.logger)
        self.superadmin_manager = SuperAdminManager(self.logger)
        self.menu_handler = MenuHandler(self.user_manager, self.member_manager, self.consultant_manager, self.systemadmin_manager, self.superadmin_manager)
        self.max_login_attempts = 3
        self.wait_time_seconds = 10
        self.failed_attempts = 0

    def run(self):
        while True:
            option = main_menu()
            if option == '1':
                username = input("Enter username: ")
                password = getpass("Your keyboard is not broken the letters are hidden \nEnter password : ")
                role = self.user_manager.authenticate_user(username, password)
                if role:
                    self.logger.set_current_user(username)
                    self.logger.log_activity("login attempt", "Successful")
                    self.menu_handler.display_role_based_menu(role)
                    self.failed_attempts = 0
                else:
                    self.logger.log_activity(f"{username} login attempt", "Failed")
                    self.failed_attempts += 1
                    input("Invalid credentials. Press enter to try again.")
                    if self.failed_attempts >= self.max_login_attempts:
                        print(f"Maximum login attempts reached. Please wait for {self.wait_time_seconds} seconds.")
                        time.sleep(self.wait_time_seconds)
                        self.failed_attempts = 0
            elif option == '2':
                self.user_manager.close()
                break
            else:
                print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    app = Application()
    app.run()
