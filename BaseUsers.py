import sqlite3

import input_checker as ic
from encryption import RSAEncryption
from StaticMethods import StaticMethods as SM 

class BaseUsers:
    def __init__(self, log_manager):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.log_manager = log_manager
        self.current_user = None

    def get_user_role(self, username):
        sql = 'SELECT username, password, role FROM users'
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        for encrypted_username,passw, role in users:
            try:
                decrypted_username = RSAEncryption.decrypt_data(encrypted_username)
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                continue
            
            if decrypted_username == username:
                return role
            
        return None

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
            new_password = ic.validate_password_input("Enter new password: ")
            rowidusers = SM.GetRowIDUsers(self.cursor, current_user)
            rowidrole = SM.GetRowIDRole(self.cursor, current_user, user_table)
            
            sql = f'UPDATE {user_table} SET password = ? WHERE rowid = ?'
            sql2 = 'UPDATE users SET password = ? WHERE rowid = ?'
            try:
                self.cursor.execute(sql, (new_password, rowidrole))
                self.cursor.execute(sql2, (new_password, rowidusers))
                self.conn.commit()
                self.conn.close()
                self.log_manager.log_activity(f"Updated password for {current_user}", "Successful")
                input("Password updated successfully. Press Enter to continue.")
            except sqlite3.IntegrityError:
                self.log_manager.log_activity(f"Failed to update password for {current_user}", "IntegrityError")
        else:
            print("User role not found. Password update failed.")
            self.log_manager.log_activity(f"Failed to update password for {current_user}", "RoleNotFound")