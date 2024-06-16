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
