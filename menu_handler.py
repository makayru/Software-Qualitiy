from menus import super_admin_menu, system_admin_menu, consultant_menu, default_menu
import os
from logger import LoggerDatabaseManager as Logger
from Display import backup_menu

class MenuHandler:
    def __init__(self, user_manager, member_manager, consultant_manager, systemadmin_manager):
        self.user_manager = user_manager
        self.member_manager = member_manager
        self.consultant_manager = consultant_manager
        self.systemadmin_manager = systemadmin_manager
        self.logger = Logger()

    def display_role_based_menu(self, role):
        if role == 'Super_Administrator':
            self.super_admin_menu()
        elif role == 'SystemAdmin':
            self.system_admin_menu()
        elif role == 'Consultant':
            self.consultant_menu()
        else:
            self.default_menu()

    def super_admin_menu(self):
        while True:
            os.system('cls')
            option = super_admin_menu()
            if option == '1':
                self.systemadmin_manager.update_password()
            elif option == '2':
                self.user_manager.view_users()
            elif option == '3':
                while True:
                    self.clear_console()
                    print(" Member management")
                    print("1. Add member")
                    print("2. Edit member")
                    print("3. Delete member")
                    print("4. View members")
                    print("5. search members")
                    print("6. Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.member_manager.register_member()
                    elif option == '2':
                        self.member_manager.edit_member()
                    elif option == '3':
                        self.member_manager.remove_member()
                    elif option == '4':
                        self.user_manager.view_table('members')
                    elif option == '5':
                        self.member_manager.search_members()
                    elif option == '6':
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif option == '4':
                while True:
                    self.clear_console()
                    print("Consultant management")
                    print("1.   Add Consultant")
                    print("2.   Edit Consultant")
                    print("3.   Delete Consultant")
                    print("4.   Reset consultant password (temporary)")
                    print("5.   Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.consultant_manager.register_consultant()
                    elif option == '2':
                        self.user_manager.edit_user("consultants")
                    elif option == '3':
                        self.user_manager.remove_user("consultants")
                    elif option == '4':
                        self.consultant_manager.temp_password_Con()
                    elif option == '5':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif option == '5':
                
                while True:
                    self.clear_console()
                    print("System Admin management")
                    print("1.   Add System Admin")
                    print("2.   Edit System Admin")
                    print("3.   Delete System Admin")
                    print("4.   Reset System admin password (temporary)")
                    print("5.   Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.systemadmin_manager.register_SA()
                    elif option == '2':
                        self.user_manager.edit_user("system_admins")
                    elif option == '3':
                        self.user_manager.remove_user("system_admins")
                    elif option == '4':
                        self.systemadmin_manager.temp_password_SA()
                    elif option == '5':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif option == '6':
                self.clear_console()
                print(backup_menu())
                print("1. Create backup")
                print("2. Restore backup")
                print("3. Back")
                option = input("Choose an option: ")
                if option == '1':
                    self.systemadmin_manager.create_backup(False)
                elif option == '2':
                    self.systemadmin_manager.restore_backup()
                elif option == '3':
                    print("Invalid choice. Please try again.")
            elif option == '7':
                self.logger.view_logs()
            elif option == '8':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def system_admin_menu(self):
        while True:
            os.system('cls')
            option = system_admin_menu()
            if option == '1':
                self.systemadmin_manager.update_password()
            elif option == '2':
                self.user_manager.view_users()
            elif option == '3':
                while True:
                    self.clear_console()
                    print(" Member management")
                    print("1. Add member")
                    print("2. Edit member")
                    print("3. Delete member")
                    print("4. View members")
                    print("5. search members")
                    print("6. Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.member_manager.register_member()
                    elif option == '2':
                        self.member_manager.edit_member()
                    elif option == '3':
                        self.member_manager.remove_member()
                    elif option == '4':
                        self.user_manager.view_table('members')
                    elif option == '5':
                        self.member_manager.search_members()
                    elif option == '6':
                        break
                    else:
                        print("Invalid choice. Please try again.")

            elif option == '4':
                while True:
                    self.clear_console()
                    print("Consultant management")
                    print("1.   Add Consultant")
                    print("2.   Edit Consultant")
                    print("3.   Delete Consultant")
                    print("4.   Reset consultant password (temporary)")
                    print("5.   Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.consultant_manager.register_consultant()
                    elif option == '2':
                        self.user_manager.edit_user("consultants")
                    elif option == '3':
                        self.user_manager.remove_user("consultants")
                    elif option == '4':
                        self.consultant_manager.temp_password_Con()
                    elif option == '5':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif option == '5':
                print(backup_menu())
                print("1. Create backup")
                print("2. Restore backup")
                print("3. Back")
                option = input("Choose an option: ")
                if option == '1':
                    self.systemadmin_manager.create_backup(False)
                elif option == '2':
                    self.systemadmin_manager.restore_backup()
                elif option == '3':
                    break
            elif option == '6':
                self.logger.view_logs()
            elif option == '7':
                break
            else:
                print("Invalid choice. Please try again.")

    def consultant_menu(self):
        while True:
            os.system('cls')
            option = consultant_menu()
            if option == '1':
                self.consultant_manager.update_password()
            elif option == '2':
                self.member_manager.register_member()
            elif option == '3':
                self.member_manager.edit_member()
            elif option == '4':
                self.member_manager.search_members()
            elif option == '5':
                break
            else:
                print("Invalid choice. Please try again.")
                
            
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def default_menu(self):
        os.system('cls')
        while True:
            option = default_menu()
            if option == '1':
                print("Viewing profile (feature to be implemented)")
            elif option == '2':
                print("Updating profile (feature to be implemented)")
            elif option == '3':
                break
            else:
                print("Invalid choice. Please try again.")
