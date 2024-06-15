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
    
    
    