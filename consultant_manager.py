import os
from datetime import datetime
import input_checker as ic
from BaseUsers import BaseUsers
import sqlite3
import encryption as enc

class ConsultantManager(BaseUsers):
    def __init__(self, log_manager):
        super().__init__(log_manager)
        self.encryption = enc.RSAEncryption()

    def register_consultant(self):
        username = ic.validate_and_get_unique_username("Enter username: ")
        password = ic.validate_password_input("Enter password: ")
        first_name = ic.validate_fname_or_lname_input("Enter first name: ")
        last_name = ic.validate_fname_or_lname_input("Enter last name: ")
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        role = 'Consultant'

        try:
            # Encrypt the password before storing it
            encrypted_username = self.encryption.encrypt_data(username)
            

            sql = 'INSERT INTO consultants (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'
            sql2 = 'INSERT INTO users (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'

            # Assuming the username does not need encryption in this case, if needed adjust accordingly
            self.cursor.execute(sql, (encrypted_username, password, first_name, last_name, registration_date, role))
            self.cursor.execute(sql2, (encrypted_username, password, first_name, last_name, registration_date, role))
            self.conn.commit()

            self.log_manager.log_activity(f"Registered consultant {username}", "Successful")
        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to register consultant {username}", "IntegrityError")

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def temp_password_Con(self):
        username = input ("Enter username: ")
        result = ic.reset_password_SystemAdmin(username)
        if result:
            self.log_manager.log_activity(f"Reset password for Consultant {username}", "Successful")
        else:
            self.log_manager.log_activity(f"Failed to reset password for Consultant {username}", "Failed")

        
        

