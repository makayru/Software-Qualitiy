# consultant_manager.py
import os
from datetime import datetime
import input_checker as ic
import sqlite3

class ConsultantManager:
    def __init__(self, log_manager):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.log_manager = log_manager
        self.current_user = None

    def register_consultant(self):
        username = ic.validate_and_get_unique_username("Enter username: ")
        password = ic.validate_password_input("Enter password: ")
        role = 'Consultant'

        sql = 'INSERT INTO consultants (username, password, role) VALUES (?, ?, ?)'
        sql2 = 'INSERT INTO users (username, password, role) VALUES (?, ?, ?)'
        try:
            self.cursor.execute(sql, (username, password, role))
            self.cursor.execute(sql2, (username, password, role))
            self.conn.commit()
            self.log_manager.log_activity(f"Registered consultant {username}", "Successful")
        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to register consultant {username}", "IntegrityError")
    
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

    def fetch_members(self):
        # Fetch a list of members from the database
        sql_select = 'SELECT * FROM members'
        self.cursor.execute(sql_select)
        members = self.cursor.fetchall()
        return members
    
