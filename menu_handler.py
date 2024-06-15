from getpass import getpass
from menus import super_admin_menu, system_admin_menu, consultant_menu, default_menu
import os

class MenuHandler:
    def __init__(self, user_manager, member_manager):
        self.user_manager = user_manager
        self.member_manager = member_manager

    def display_role_based_menu(self, role):
        if role == 'Super_Administrator':
            self.super_admin_menu()
        elif role == 'System_Admin':
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
                print("Viewing all users (feature to be implemented)")
            elif option == '2':
                print("What role do you want to assign to the new user? \n 1. Consultant \n 2. System Admin \n 3. Member")
                role = input("Choose an option: ")
                if role == '1':
                    print("Registering new Consultant (feature to be implemented)")
                elif role == '2':
                    print("Registering new System Admin (feature to be implemented)")
                elif role == '3':
                    self.member_manager.register_member()
                else:
                    print("Invalid choice. Please try again.")
                    
                
                
            elif option == '3':
                print("Editing user (feature to be implemented)")
            elif option == '4':
                print("Deleting user (feature to be implemented)")
            elif option == '5':
                print("Resetting user password (feature to be implemented)")
            elif option == '6':
                print("Backup and Restore (feature to be implemented)")
            elif option == '7':
                print("Viewing logs (feature to be implemented)")
            elif option == '8':
                print("Searching members (feature to be implemented)")
            elif option == '9':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def system_admin_menu(self):
        while True:
            os.system('cls')
            option = system_admin_menu()
            if option == '1':
                print("Updating password (feature to be implemented)")
            elif option == '2':
                print("Viewing users (feature to be implemented)")
            elif option == '3':
                print("Adding user (feature to be implemented)")
            elif option == '4':
                print("Edit user (feature to be implemented)")
            elif option == '5':
                print("Delete user (feature to be implemented)")
            elif option == '6':
                print("Reset user password (feature to be implemented)")
            elif option == '7':
                print("Backup and Restore (feature to be implemented)")
            elif option == '8':
                print("Viewing logs (feature to be implemented)")
            elif option == '9':
                print("Searching members (feature to be implemented)")
            elif option == '10':
                break
            else:
                print("Invalid choice. Please try again.")

    def consultant_menu(self):
        while True:
            os.system('cls')
            option = consultant_menu()
            if option == '1':
                print("Updating password (feature to be implemented)")
            elif option == '2':
                print("Adding member (feature to be implemented)")
            elif option == '3':
                print("Editing member (feature to be implemented)")
            elif option == '4':
                print("Searching member (feature to be implemented)")
            elif option == '5':
                break
            else:
                print("Invalid choice. Please try again.")
                
            


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
