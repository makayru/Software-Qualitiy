import os
from datetime import datetime
import input_checker as ic
import sqlite3

class SystemAdminManager:
    def __init__(self, log_manager):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.log_manager = log_manager
        self.current_user = log_manager.current_user
        
    def register_SA(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        role = 'SystemAdmin'
        
        sql = 'INSERT INTO system_admins (username, password, role) VALUES (?, ?, ?)'   
        sql2 = 'INSERT INTO users (username, password, role) VALUES (?, ?, ?)'
        try:
            self.cursor.execute(sql, (username, password, role))
            self.cursor.execute(sql2, (username, password, role))
            self.conn.commit()
            self.log_manager.log_activity(f"Registered system admin {username}", "Successful")
        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to register system admin {username}", "IntegrityError")
    
    def update_password(self):
        current_user = self.log_manager.current_user
        password = ic.validate_password_input("Enter new password: ")
        sql = 'UPDATE consultants SET password = ? WHERE username = ?'
        sql2 = 'UPDATE users SET password = ? WHERE username = ?'
        try:
            self.cursor.execute(sql, (password,current_user))
            self.cursor.execute(sql2, (password,current_user))
            self.conn.commit()
            self.log_manager.log_activity(f"Updated password for consultant {self.current_user}", "Successful")
            input("Password updated successfully. Press Enter to continue.")

        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to update password for consultant {self.current_user}", "IntegrityError")
            input("Password updated successfully. Press Enter to continue.")

    