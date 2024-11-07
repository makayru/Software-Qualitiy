import os
from datetime import datetime
import input_checker as ic
from consultant_manager import BaseUsers
import sqlite3
import encryption as enc
import zipfile
import os
from Display import backup_menu as bm


class SystemAdminManager(BaseUsers):
    def __init__(self, log_manager):
        super().__init__(log_manager)
        self.encryption = enc.RSAEncryption()


    def register_SA(self):
        username = ic.validate_and_get_unique_username("Enter username: ")
        password = ic.validate_password_input("Enter password: ")
        firstname = ic.validate_fname_or_lname_input("Enter first name: ")
        lastname = ic.validate_fname_or_lname_input("Enter last name: ")
        role = 'SystemAdmin'
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        try:
            encrypted_username = self.encryption.encrypt_data(username)
    
            sql_users = 'INSERT INTO users (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)'
            self.cursor.execute(sql_users, (encrypted_username, password, firstname, lastname, registration_date, role))
            user_id = self.cursor.lastrowid 
    
            sql_system_admins = 'INSERT INTO system_admins (user_id, username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?, ?)'
            self.cursor.execute(sql_system_admins, (user_id, encrypted_username, password, firstname, lastname, registration_date, role))
    
            self.conn.commit()
    
            self.log_manager.log_activity(f"Registered system admin {username}", "Successful")
            print(f"System Admin {username} registered successfully.")
        except sqlite3.IntegrityError:
            self.log_manager.log_activity(f"Failed to register system admin {username}", "IntegrityError")
            print(f"Failed to register system admin {username}. Integrity Error.")
    

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
    
    def temp_password_SA(self):
        username = input ("Enter username: ")
        result = ic.reset_password_SystemAdmin(username)
        if result:
            self.log_manager.log_activity(f"Reset password for System Admin {username}", "Successful")
        else:
            self.log_manager.log_activity(f"Failed to reset password for System Admin {username}", "Failed")


    def create_backup(self, backup_restore):
        backup_dir = "backups"
        files_to_backup = ['logs.db', 'unique_meal.db']
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        if backup_restore == False:
            backup_name = datetime.now().strftime("backup_%Y-%m-%d_%H-%M-%S.zip")
        else:
            backup_name = datetime.now().strftime("backup_before_restoring_%Y-%m-%d_%H-%M-%S.zip")
        
        backup_path = os.path.join(backup_dir, backup_name)
        
        with zipfile.ZipFile(backup_path, 'w') as backup_zip:
            for file in files_to_backup:
                if os.path.exists(file):
                    backup_zip.write(file, os.path.basename(file))
                else:
                    input(f"Warning: {file} not found and won't be included in the backup. Press Enter to continue...")
        
        input(f"Backup created successfully: {backup_path}. Press Enter to continue...")

    def restore_backup_logic(self, backup_zip_path, backup_current):
        restore_dir="."
        if backup_current:
            while True:
                user_choice = input("\nDo you want to backup your current database files to prevent data loss? (y/n): ").lower()
                if user_choice == 'y':
                 
                    print("\nBacking up current database files...")
                    self.create_backup(True)  
                    print("\nCurrent database backup created successfully.\n")
                    break 
                elif user_choice == 'n':
                    print("Proceeding without backing up current database files.")
                    break 
                else:
                    print("Invalid input. Please enter 'y' for Yes or 'n' for No.")
        
        if not os.path.exists(backup_zip_path):
            input(f"Error: Backup file {backup_zip_path} does not exist. Press Enter to return...")
            return
        
        if not os.path.exists(restore_dir):
            os.makedirs(restore_dir)
        
        try:
            with zipfile.ZipFile(backup_zip_path, 'r') as backup_zip:
                backup_zip.extractall(restore_dir)
                input(f"Backup successfully restored to {backup_zip_path}. Press Enter to continue...")
        except zipfile.BadZipFile:
            input(f"Error: The file {backup_zip_path} is not a valid ZIP file. Press Enter to return...")
        except Exception as e:
            input(f"Error occurred while restoring backup: {e}. Press Enter to return...")


    def restore_backup(self, batch_size=10):
        backups_dir="backups"
        backups = []
        for f in os.listdir(backups_dir):
            if f.endswith(".zip"):
                backups.append(f)
        

        total_backups = len(backups)
        total_batches = (total_backups // batch_size) + (1 if total_backups % batch_size > 0 else 0)
        
        current_batch = 0

        if total_backups == 0:
            input("No backups found. Press Enter to return...")
            return  
        while current_batch < total_batches:
            start_index = current_batch * batch_size
            end_index = min((current_batch + 1) * batch_size, total_backups)
            self.clear_console()
            print(bm())
            print(f"\nShowing backups {start_index + 1} to {end_index}:")
            
            for i in range(start_index, end_index):
                print(f"{i + 1}. {backups[i]}")

            user_input = input("\nEnter the number of the backup to restore, 'n' for next, 'p' for previous, or 'q' to quit: ").lower()

            if user_input == 'n':
                self.clear_console()
                if current_batch < total_batches - 1:
                    current_batch += 1
                else:
                    current_batch = 0 
            
            elif user_input == 'p':
                self.clear_console()
                if current_batch == 0:
                    current_batch = total_batches - 1
                else:
                    current_batch -= 1

            elif user_input == 'q':
                print("Exiting without restoring a backup.")
                break
            
            elif user_input.isdigit():
                backup_index = int(user_input) - 1
                if 0 <= backup_index < total_backups:
                    selected_backup = backups[backup_index]
                    backup_zip_path = os.path.join(backups_dir, selected_backup)
                    input(f"Selected backup: {selected_backup}. Press Enter to continue...")
                    self.restore_backup_logic(backup_zip_path, True) 
                    break  
                
                else:
                    self.clear_console()
                    print("Invalid number. Please select a number from the list.")
            
            else:
                self.clear_console()
                print("Invalid input. Please try again.")



    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')