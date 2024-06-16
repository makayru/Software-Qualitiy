import os
from datetime import datetime
import input_checker as ic
from BaseUsers import BaseUsers
import sqlite3


class SystemAdminManager(BaseUsers):
    def __init__(self, log_manager):
        super().__init__(log_manager)

    def register_SA(self):
        username = ic.validate_and_get_unique_username("Enter username: ")
        password = ic.validate_password_input("Enter password: ")
        firstname = ic.validate_fname_or_lname_input("Enter first name: ")
        lastname = ic.validate_fname_or_lname_input("Enter last name: ")
        role = 'SystemAdmin'
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sql = 'INSERT INTO system_admins (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'   
        sql2 = 'INSERT INTO users (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (username, password,firstname, lastname, registration_date , role))
            self.cursor.execute(sql2, (username, password, firstname, lastname, registration_date, role))
            self.conn.commit()
            self.log_manager.log_activity(f"Registered system admin {username}", "Successful")
        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to register system admin {username}", "IntegrityError")
#users
    def fetch_users(self):
        sql_select = 'SELECT username, first_name, last_name, registration_date, role FROM users'
        self.cursor.execute(sql_select)
        members = self.cursor.fetchall()
        self.conn.commit()
        return members  

    def view_users(self):
        users = self.fetch_users()
        if not users:
            print("No users found")
        else:
            print("\nUsers:\n")
            for user in users:
                username, first_name, last_name, registration_date, role = user
                print(f"Username: {username}")
                print(f"Full Name: {first_name} {last_name}")
                print(f"Registration Date: {registration_date}")
                print(f"Role: {role}")
                print("-" * 20)
            
            input("Press any key to continue...")
            os.system('cls' if os.name == 'nt' else 'clear') 
    
    def search_users_querry(self, search_key):
        search_key = f"%{search_key}%"
        sql = '''SELECT * FROM users WHERE username LIKE ?'
                OR first_name LIKE ? OR last_name LIKE ?
                OR registration_date LIKE ? OR role LIKE ?'''
        self.cursor.execute(sql, (search_key, search_key, search_key, search_key, search_key))
        results = self.cursor.fetchall()
        return results
    
    def search_users(self, search_key):
        results = self.search_users_querry(search_key)
        if not results:
            print("No results found")
        else:
            print("Results:")
            for result in results:
                user_id, username, first_name, last_name, registration_date, role = result
                print(f"User ID: {user_id}")
                print(f"Username: {username}")
                print(f"Full Name: {first_name} {last_name}")
                print(f"Registration Date: {registration_date}")
                print(f"Role: {role}")
                print("-" * 20)
#consultants
    def edit_consultant(self):
            while True:
                self.clear_console()

                search_key = input("Enter search keyword (consultant ID, first name, last name, etc.): ").strip()
                results = self.search_consultants_query(search_key)

                if len(results) > 10:
                    print("More than 10 consultants found. Please refine your search.")
                elif len(results) == 0:
                    print("No matching consultants found.")
                else:
                    selected_consultant = self.select_consultant_from_results(results)
                    if selected_consultant:
                        self.edit_consultant_details(selected_consultant)

                if input("Do you want to edit anything else? (yes/no): ").strip().lower() != 'yes':
                    break

    def edit_consultant_details(self, selected_consultant):
        consultant_id = selected_consultant[0]
        username = selected_consultant[1]
        field_updated = False

        while True:
            self.clear_console()
            print(f"Editing consultant ID {consultant_id}:")
            print("-----------------------------")
            print(f"1. Username: {selected_consultant[1]}")
            print(f"2. Password: {selected_consultant[2]}")
            print(f"3. Firstname: {selected_consultant[3]}")
            print(f"4. Lastname: {selected_consultant[4]}")
            print(f"5. Registration Date: {selected_consultant[5]}")
            print(f"6. Role: {selected_consultant[6]}")
            print("-----------------------------")

            field_choice = input("Enter the number of the field to edit (or '0' to finish editing this consultant): ").strip()

            if field_choice == '0':
                print("Finished editing this consultant.")
                break
            elif field_choice in {'1', '2', '3', '4', '5', '6'}:
                new_value = None
                field_name = None
                if field_choice == '1':
                    new_value = ic.validate_and_get_unique_username("Enter new User name: ")
                    field_name = 'username'
                elif field_choice == '2':
                    new_value = ic.validate_password_input("Enter new password name: ")
                    field_name = 'password'
                elif field_choice == '3':
                    new_value = ic.validate_fname_or_lname_input("Enter first name: ")
                    field_name = 'first_name'
                elif field_choice == '4':
                    new_value = ic.validate_fname_or_lname_input("Enter last name: ")
                    field_name = 'last_name'
                elif field_choice == '5':
                    print("Registration date cannot be edited.")
                    input("Press any key to continue...")
                    continue
                elif field_choice == '6':
                    print("Authorisation to change role denied")
                    input("Press any key to continue...")
                    continue

                if new_value is not None and field_name is not None:
                    sql_update = f'UPDATE consultants SET {field_name} = ? WHERE id = ?'
                    sql_update2 = f'UPDATE users SET {field_name} = ? WHERE username = ?'
                    self.cursor.execute(sql_update, (new_value, consultant_id))
                    self.cursor.execute(sql_update2, (new_value, username))

                    self.conn.commit()
                    self.log_manager.log_activity(f"Updated {field_name} for consultant {consultant_id}", "Successful")

                    # Convert selected_consultant tuple to list, update value, and convert back to tuple
                    selected_consultant = list(selected_consultant)
                    selected_consultant[int(field_choice)] = new_value  # Convert field_choice to int
                    selected_consultant = tuple(selected_consultant)

                    print(f"{field_name.capitalize()} updated to: {new_value}")
                    field_updated = True
            else:
                print("Invalid choice. Please enter a number from the menu.")

        if field_updated:
            if input("Do you want to edit anything else for this consultant? (yes/no): ").strip().lower() != 'yes':
                return

    def remove_consultant(self):
        while True:
            self.clear_console()

            search_key = input("Enter search keyword (consultant ID, first name, last name, etc.): ").strip()
            results = self.search_consultants_query(search_key)

            if len(results) > 10:
                print("More than 10 consultants found. Please refine your search.")
            elif len(results) == 0:
                print("No matching consultants found.")
            else:
                selected_consultant = self.select_consultant_from_results(results)
                if selected_consultant:
                    self.delete_consultant(selected_consultant[0], selected_consultant[1])

            if input("Do you want to remove another consultant? (yes/no): ").strip().lower() != 'yes':
                break

    def delete_consultant(self, consultant_id, username):
        confirmation = input(f"Are you sure you want to delete consultant ID {consultant_id}? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            sql_delete = 'DELETE FROM consultants WHERE id = ?'
            sql_delete2 = 'DELETE FROM users WHERE username = ?'

            self.cursor.execute(sql_delete, (consultant_id,))
            self.cursor.execute(sql_delete2, (username,))

            self.conn.commit()
            self.log_manager.log_activity(f"Deleted consultant ID {consultant_id}", "Successful")
            print(f"Consultant ID {consultant_id} deleted.")
        else:
            print("Deletion canceled.")

    def search_consultants_query(self, search_key):
        search_key = f"%{search_key}%"
        sql = '''SELECT * FROM consultants WHERE id LIKE ? 
                 OR username LIKE ? OR first_name LIKE ? OR last_name LIKE ? 
                 OR registration_date LIKE ?'''
        self.cursor.execute(sql, (search_key,search_key , search_key, search_key, search_key))
        results = self.cursor.fetchall()
        return results

    def search_consultants(self, search_key):
        results = self.search_consultants_query(search_key)
        if results:
            print("Search Results:")
            for result in results:
                id, username, firstname, lastname, registration_date, role = result
                print(f"Consultant ID: {id}")
                print(f"Username: {username}")
                print(f"Name: {firstname} {lastname}")
                print(f"Registration Date: {registration_date}")
                print(f"Role: {role}")
                print("-" * 20)
        else:
            print("No matching consultants found.")

    def select_consultant_from_results(self, results):
        while True:
            try:
                self.clear_console()
                print("Search Results:")
                for index, row in enumerate(results, start=1):
                    id, username,password ,firstname, lastname, registration_date, role= row
                    print(f"{index}. ID: {id},Username : {username}, Name: {firstname} {lastname}")

                choice = int(input("Enter the number of the consultant to select (or '0' to cancel): ").strip())
                if choice == 0:
                    print("Canceled.")
                    return None
                elif 1 <= choice <= len(results):
                    return results[choice - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def temporary_password(self):
        while True:
            self.clear_console()
            search_key = input("Enter search keyword (consultant ID, first name, last name, etc.): ").strip()
            results = self.search_consultants_query(search_key)

            if len(results) > 10:
                print("More than 10 consultants found. Please refine your search.")
            elif len(results) == 0:
                print("No matching consultants found.")
            else:
                selected_consultant = self.select_consultant_from_results(results)
                if selected_consultant:
                    self.reset_consultant_password(selected_consultant[0], selected_consultant[1])

            if input("Do you want to reset another consultant's password? (yes/no): ").strip().lower() != 'yes':
                break

    def reset_consultant_password(self, consultant_id, username):
        new_password = ic.generate_random_password()
        sql_update = 'UPDATE consultants SET password = ? WHERE id = ?'
        sql_update2 = 'UPDATE users SET password = ? WHERE username = ?'

        self.cursor.execute(sql_update, (new_password, consultant_id))
        self.cursor.execute(sql_update2, (new_password, username))

        self.conn.commit()
        self.log_manager.log_activity(f"Reset password for consultant ID {consultant_id}", "Successful")
        print(f"Password for consultant ID {consultant_id} reset.") 
        print(f"New password: {new_password}")
        input("Write down the new password and press any key to continue...")
        
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')