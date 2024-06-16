import sqlite3
from datetime import datetime
import input_checker as ic

class BaseUsers:
    def __init__(self, log_manager):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.log_manager = log_manager
        self.current_user = None

    def get_user_role(self, username):
        sql = 'SELECT role FROM users WHERE username = ?'
        self.cursor.execute(sql, (username,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    
    def get_user_table(self, role):
        role_table_map = {
            'Consultant': 'consultants',
            'SystemAdmin': 'system_admins',
            'SuperAdmin': 'super_admins'
        }
        return role_table_map.get(role)

    def update_password(self):
        current_user = self.log_manager.current_user
        user_role = self.get_user_role(current_user)

        if user_role:
            user_table = self.get_user_table(user_role)
            new_password = ic.validate_password_input("\n----------------\nEnter new password: ")
            sql = f'UPDATE {user_table} SET password = ? WHERE username = ?'
            sql2 = 'UPDATE users SET password = ? WHERE username = ?'
            try:
                self.cursor.execute(sql, (new_password, current_user))
                self.cursor.execute(sql2, (new_password, current_user))
                self.conn.commit()
                self.log_manager.log_activity(f"Updated password for {current_user}", "Successful")
                input("Password updated successfully. Press Enter to continue.")
            except sqlite3.IntegrityError:
                self.log_manager.log_activity(f"Failed to update password for {current_user}", "IntegrityError")
        else:
            print("User role not found. Password update failed.")
            self.log_manager.log_activity(f"Failed to update password for {current_user}", "RoleNotFound")