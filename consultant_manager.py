# consultant_manager.py
import os
from datetime import datetime
import input_checker as ic
from BaseUsers import BaseUsers
import sqlite3

class ConsultantManager(BaseUsers):
    def __init__(self, log_manager):
        super().__init__(log_manager)

    def register_consultant(self):
        username = ic.validate_and_get_unique_username("Enter username: ")
        password = ic.validate_password_input("Enter password: ")
        first_name = ic.validate_fname_or_lname_input("Enter first name: ")
        last_name = ic.validate_fname_or_lname_input("Enter last name: ")
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        role = 'Consultant'

        sql = 'INSERT INTO consultants (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'
        sql2 = 'INSERT INTO users (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (username, password, first_name, last_name, registration_date, role))
            self.cursor.execute(sql2, (username, password, first_name, last_name, registration_date, role))
            self.conn.commit()
            self.log_manager.log_activity(f"Registered consultant {username}", "Successful")
        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to register consultant {username}", "IntegrityError")
    