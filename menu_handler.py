from getpass import getpass
from menus import super_admin_menu, system_admin_menu, consultant_menu, default_menu
import os

class MenuHandler:
    def __init__(self, user_manager, member_manager, consultant_manager, systemadmin_manager, super_admin_manager):
        self.user_manager = user_manager
        self.member_manager = member_manager
        self.consultant_manager = consultant_manager
        self.systemadmin_manager = systemadmin_manager
        self.super_admin_manager = super_admin_manager

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
                self.super_admin_manager.update_password()
            elif option == '2':
                self.super_admin_manager.view_users()
            elif option == '3':
                while True:
                    self.clear_console()
                    print(" Member management")
                    print("1. Add member")
                    print("2. Edit member")
                    print("3. Delete member")
                    print("4. View members")
                    print("5. Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.member_manager.register_member()
                    elif option == '2':
                        self.member_manager.edit_member()
                    elif option == '3':
                        self.member_manager.remove_member()
                    elif option == '4':
                        search_key = input("Enter search key: ")
                        self.member_manager.search_members(search_key)
                    elif option == '5':
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
                        self.systemadmin_manager.register_consultant()
                    elif option == '2':
                        print("Editing consultant (feature to be implemented)")
                    elif option == '3':
                        print("Deleting consultant (feature to be implemented)")
                    elif option == '4':
                        print("Resetting consultant password (feature to be implemented)")
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
                        print("Editing system admin (feature to be implemented)")
                    elif option == '3':
                        print("Deleting system admin (feature to be implemented)")
                    elif option == '4':
                        print("Resetting system admin password (feature to be implemented)")
                    elif option == '5':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif option == '5':
                print("Resetting user password (feature to be implemented)")
            elif option == '6':
                print("Backup and Restore (feature to be implemented)")
            elif option == '7':
                print("Viewing logs (feature to be implemented)")
            elif option == '8':
                search_key = input("Enter search key: ")
                self.member_manager.search_members(search_key)

            elif option == '9':
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
                self.systemadmin_manager.view_users()
            elif option == '3':
                while True:
                    self.clear_console()
                    print(" Member management")
                    print("1. Add member")
                    print("2. Edit member")
                    print("3. Delete member")
                    print("4. Search members")
                    print("5. Back")
                    option = input("Choose an option: ")
                    if option == '1':
                        self.member_manager.register_member()
                    elif option == '2':
                        self.member_manager.edit_member()
                    elif option == '3':
                        self.member_manager.remove_member()
                    elif option == '4':
                        search_key = input("Enter search key: ")
                        self.member_manager.search_members(search_key)
                    elif option == '5':
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
                        self.systemadmin_manager.edit_user("consultant")
                    elif option == '3':
                        self.systemadmin_manager.remove_user("consultant")
                    elif option == '4':
                        self.systemadmin_manager.temporary_password()
                    elif option == '5':
                        break
                    else:
                        print("Invalid choice. Please try again.")
            elif option == '5':
                print("Backup and Restore (feature to be implemented)")
            elif option == '6':
                print("Viewing logs (feature to be implemented)")
            elif option == '7':
                search_key = input("Enter search key: ")
                self.member_manager.search_members(search_key)
            elif option == '8':
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
                search_key = input("Enter search key: ")
                self.member_manager.search_members(search_key)
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
