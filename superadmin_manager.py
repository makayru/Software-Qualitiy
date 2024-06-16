from systemadmin_manager import SystemAdminManager
import os
from datetime import datetime
import input_checker as ic
from BaseUsers import BaseUsers
import sqlite3

class SuperAdminManager(SystemAdminManager):
    def __init__(self, log_manager):
        super().__init__(log_manager)

    def search_sa_querry(self, search_key):
            search_key = f"%{search_key}%"
            sql = '''SELECT * FROM system_admins WHERE username LIKE ? 
                    OR first_name LIKE ? OR last_name LIKE ? 
                    OR registration_date LIKE ? OR role LIKE ?'''
            self.cursor.execute(sql, (search_key, search_key, search_key, search_key, search_key))
            results = self.cursor.fetchall()
            return results

    def search_sa(self, search_key):
        results = self.search_sa_querry(search_key)
        if results:
            print("Search Results:")
            for result in results:
                sa_id, username, firstname, lastname, registration_date, role = result
                print(f"System Admin ID: {sa_id}")
                print(f"Username: {username}")
                print(f"Name: {firstname} {lastname}")
                print(f"Registration Date: {registration_date}")
                print(f"Role: {role}")
                print("-" * 20)
        else:
            print("No matching system admins found.")

    def edit_sa(self):
        while True:
            self.clear_console()

            search_key = input("Enter search keyword (system admin ID, username, first name, last name, etc.): ").strip()
            results = self.search_sa_querry(search_key)

            if len(results) > 10:
                print("More than 10 system admins found. Please refine your search.")
            elif len(results) == 0:
                print("No matching system admins found.")
            else:
                selected_sa = self.select_sa_from_results(results)
                if selected_sa:
                    self.edit_sa_details(selected_sa)

            if input("Do you want to edit anything else? (yes/no): ").strip().lower() != 'yes':
                break

    def remove_sa(self):
        while True:
            self.clear_console()

            search_key = input("Enter search keyword (system admin ID, username, first name, last name, etc.): ").strip()
            results = self.search_sa_querry(search_key)

            if len(results) > 10:
                print("More than 10 system admins found. Please refine your search.")
            elif len(results) == 0:
                print("No matching system admins found.")
            else:
                selected_sa = self.select_sa_from_results(results)
                if selected_sa:
                    self.delete_sa(selected_sa[0])

            if input("Do you want to remove another system admin? (yes/no): ").strip().lower() != 'yes':
                break

    def select_sa_from_results(self, results):
        while True:
            try:
                self.clear_console()
                print("Search Results:")
                for index, row in enumerate(results, start=1):
                    sa_id, username, firstname, lastname, registration_date, role = row
                    print(f"{index}. ID: {sa_id}, Username: {username}")

                choice = int(input("Enter the number of the system admin to select (or '0' to cancel): ").strip())
                if choice == 0:
                    print("Canceled.")
                    return None
                elif 1 <= choice <= len(results):
                    return results[choice - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def edit_sa_details(self, selected_sa):
        sa_id = selected_sa[0]
        field_updated = False

        while True:
            self.clear_console()
            print(f"Editing system admin ID {sa_id}:")
            print("-----------------------------")
            print(f"1. Username: {selected_sa[1]}")
            print(f"2. Password: {selected_sa[2]}")
            print(f"3. First Name: {selected_sa[3]}")
            print(f"4. Last Name: {selected_sa[4]}")
            print(f"5. Registration Date: {selected_sa[5]}")
            print(f"6. Role: {selected_sa[6]}")
            print("-----------------------------")

            field_choice = input("Enter the number of the field to edit (or '0' to finish editing this system admin): ").strip()

            if field_choice == '0':
                print("Finished editing this system admin.")
                break
            elif field_choice in {'1', '2', '3', '4', '5', '6'	}:
                new_value = None
                field_name = None
                if field_choice == '1':
                    new_value = ic.validate_and_get_unique_username("Enter new username: ")
                    field_name = 'username'
                elif field_choice == '2':
                    new_value = ic.validate_fname_or_lname_input("Enter new first name: ")
                    field_name = 'password'
                elif field_choice == '3':
                    new_value = ic.validate_fname_or_lname_input("Enter new last name: ")
                    field_name = 'first_name'
                elif field_choice == '4':
                    new_value = ic.validate_fname_or_lname_input("Enter new last name: ")
                    field_name = 'last_name'
                elif field_choice == '5':
                    print("Registration date cannot be edited.")
                    continue
                elif field_choice == '6':
                    new_value = input("Enter new role ( systemadmin, consultant): ").strip().lower()
                    field_name = 'role' 
                    continue

                if new_value is not None and field_name is not None:
                    sql_update = f'UPDATE system_admins SET {field_name} = ? WHERE sa_id = ?'
                    self.cursor.execute(sql_update, (new_value, sa_id))
                    self.conn.commit()
                    self.log_manager.log_activity(f"Updated {field_name} for system admin ID {sa_id}", "Successful")

                    selected_sa = list(selected_sa)
                    selected_sa[int(field_choice)] = new_value
                    selected_sa = tuple(selected_sa)

                    print(f"{field_name.capitalize()} updated to: {new_value}")
                    field_updated = True
            else:
                print("Invalid choice. Please enter a number from the menu.")

        if field_updated:
            if input("Do you want to edit anything else for this system admin? (yes/no): ").strip().lower() != 'yes':
                return

    def delete_sa(self, sa_id):
        confirmation = input(f"Are you sure you want to delete system admin ID {sa_id}? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            sql_delete = 'DELETE FROM system_admins WHERE sa_id = ?'
            self.cursor.execute(sql_delete, (sa_id,))
            self.conn.commit()
            self.log_manager.log_activity(f"Deleted system admin ID {sa_id}", "Successful")
            print(f"System admin ID {sa_id} deleted.")
        else:
            print("Deletion canceled.")

    def view_sas(self):
        sql_select = 'SELECT sa_id, username, first_name, last_name, registration_date, role FROM system_admins'
        self.cursor.execute(sql_select)
        sas = self.cursor.fetchall()
        self.conn.commit()

        if not sas:
            print("No system admins found")
        else:
            print("\nSystem Admins:\n")
            for sa in sas:
                sa_id, username, first_name, last_name, registration_date, role = sa
                print(f"System Admin ID: {sa_id}")
                print(f"Username: {username}")
                print(f"Name: {first_name} {last_name}")
                print(f"Registration Date: {registration_date}")
                print(f"Role: {role}")
                print("-" * 20)

            input("Press any key to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
