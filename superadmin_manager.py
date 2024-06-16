from systemadmin_manager import SystemAdminManager
import os
from datetime import datetime
import input_checker as ic
from BaseUsers import BaseUsers
import sqlite3

class SuperAdminManager(SystemAdminManager):
    def __init__(self, log_manager):
        super().__init__(log_manager)

    def update_password(self):
        current_user = self.log_manager.current_user
        user_role = self.get_user_role(current_user)

        if user_role:
            user_table = self.get_user_table(user_role)
            new_password = ic.validate_password_input("Enter new password: ")
            sql2 = 'UPDATE users SET password = ? WHERE username = ?'
            try:
                self.cursor.execute(sql2, (new_password, current_user))
                self.conn.commit()
                self.log_manager.log_activity(f"Updated password for {current_user}", "Successful")
                input("Password updated successfully. Press Enter to continue.")
            except sqlite3.IntegrityError:
                self.log_manager.log_activity(f"Failed to update password for {current_user}", "IntegrityError")
        else:
            print("User role not found. Password update failed.")
            self.log_manager.log_activity(f"Failed to update password for {current_user}", "RoleNotFound")
            
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

