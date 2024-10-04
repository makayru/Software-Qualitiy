# user_manager.py
import sqlite3
import datetime
import logger as log
import os
import zipfile
import encryption as enc
import input_checker as ic

class UserManager:
    def __init__(self, logger):
        self.encryption = enc.RSAEncryption()
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.logger = logger
        self.create_table()
        self.current_user = None

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            weight INTEGER NOT NULL,
            address TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultants (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_admins (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            role TEXT NOT NULL
        )
        ''')
        self.conn.commit()
        
        

        # Insert default accounts if they do not exist
        self.insert_default_accounts()

    def authenticate_user(self, username, password):
        # Fetch all encrypted usernames and passwords from the database
        sql = 'SELECT username, password, role FROM users'
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        
        # Hash the input password
        hashed_input_password = self.encryption.hash_data(password)
    
        # Iterate through users and attempt decryption/authentication
        for encrypted_username, stored_password, role in users:
            try:
                decrypted_username = self.encryption.decrypt_data(encrypted_username)
            except Exception as e:
                print(f"Decryption failed: {str(e)}")
                continue  # Skip this entry if decryption fails
            
            if decrypted_username == username and stored_password == hashed_input_password:
                self.current_user = username
                print(f"Authentication successful. Role: {role}")
                self.logger.log_activity('login attempt', 'Successful')
                return role
        
        # If no match was found
        print("Authentication failed. User not found or incorrect password.")
        self.logger.log_activity('login attempt', 'Failed: User not found or incorrect password')
        return None


    

    def insert_default_accounts(self):
        """Insert default accounts with predefined credentials if they do not exist."""
        default_accounts = [
            (self.encryption.encrypt_data("super_admin"), self.encryption.hash_data("Admin_123?"), "Super_Administrator"),
        ]

        for username, password, role in default_accounts:
            self.cursor.execute('SELECT COUNT(*) FROM users WHERE username = ?', (username,))
            if self.cursor.fetchone()[0] == 0:
                self.cursor.execute('INSERT INTO users (username, password, first_name, last_name, registration_date, role) VALUES (?, ?, ?, ?, ?, ?)',
                                    (username, password,"", "", "", role))
                self.conn.commit()
                print(f"Account {username} with role {role} inserted successfully.")
                self.logger.log_activity("insert default account", "Successful")
            else:
                print(f"Account {username} already exists.")
                self.logger.log_activity( "insert default account", "Failed: Already exists")

    def create_backup(self):
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = os.path.join(backup_dir, f'backup_{timestamp}.zip')

        with zipfile.ZipFile(backup_filename, 'w') as backup_zip:
            backup_zip.write('unique_meal.db')
            backup_zip.write('logs.db')

        self.logger.log_activity(f"Created backup_{timestamp}.zip", "Successful")

    def close(self):
        self.conn.close()
    
    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')


    def edit_user(self, table_name):
        while True:
            self.clear_console()

            search_key = input(f"Enter search keyword (username, firstname, last name) for {table_name}: ").strip()
            results = self.search_users_query(search_key, table_name)

            if len(results) > 10:
                print("More than 10 users found. Please refine your search.")
            elif len(results) == 0:
                print("No matching user found.")
            else:
                selected_user = self.select_user_from_results(results)
                if selected_user:
                    self.edit_user_details(selected_user, table_name)

            if input(f"Do you want to edit anything else for {table_name}? (yes/no): ").strip().lower() != 'yes':
                break

    def search_users_query(self, search_key, table_name):
        search_key = f"%{search_key}%"
        sql = f'''SELECT * FROM {table_name} WHERE username LIKE ?
                OR first_name LIKE ? OR last_name LIKE ?
                OR registration_date LIKE ? OR role LIKE ?'''
        self.cursor.execute(sql, (search_key, search_key, search_key, search_key, search_key))
        results = self.cursor.fetchall()
        return results

    def select_user_from_results(self, results):
        while True:
            try:
                self.clear_console()
                print("Search Results:")
                for index, row in enumerate(results, start=1):
                    # Unpack the row values, including id
                    id, username, password, first_name, last_name, registration_date, role = row
                    print(f"{index}. Username: {self.encryption.decrypt_data(username)}, Full Name: {first_name} {last_name}, Registration Date: {registration_date}, Role: {role}")

                choice = int(input("Enter the number of the user to select (or '0' to cancel): ").strip())
                if choice == 0:
                    print("Canceled.")
                    return None
                elif 1 <= choice <= len(results):
                    return results[choice - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def edit_user_details(self, selected_user, table_name):
        user_id = selected_user[0]  # ID of the user
        field_updated = False

        while True:
            self.clear_console()
            print(f"Editing user ID {user_id} from {table_name}:")
            print("-----------------------------")
            print(f"1. Username: {self.encryption.decrypt_data(selected_user[1])}")  # Decrypting username
            print(f"2. First Name: {selected_user[3]}")
            print(f"3. Last Name: {selected_user[4]}")
            print(f"4. Registration Date: {selected_user[5]}")
            print(f"5. Role: {selected_user[6]}")
            print("-----------------------------")

            field_choice = input("Enter the number of the field to edit (or '0' to finish editing this user): ").strip()

            if field_choice == '0':
                print("Finished editing this user.")
                break
            elif field_choice in {'1', '2', '3', '4', '5'}:
                new_value = None
                field_name = None

                if field_choice == '1':
                    new_value = ic.validate_and_get_unique_username("Enter new username: ")
                    new_value = self.encryption.encrypt_data(new_value)  # Encrypting new username before storing
                    field_name = 'username'
                elif field_choice == '2':
                    new_value = ic.validate_fname_or_lname_input("Enter new first name: ")
                    field_name = 'first_name'
                elif field_choice == '3':
                    new_value = ic.validate_fname_or_lname_input("Enter new last name: ")
                    field_name = 'last_name'
                elif field_choice == '4':
                    new_value = input("Enter new registration date (YYYY-MM-DD): ").strip()
                    field_name = 'registration_date'
                elif field_choice == '5':
                    new_value = ic.validate_role_input("Enter new role (Consultant, SystemAdmin): ")
                    field_name = 'role'

                if new_value is not None and field_name is not None:
                    sql_update = f'UPDATE {table_name} SET {field_name} = ? WHERE id = ?'
                    self.cursor.execute(sql_update, (new_value, user_id))
                    self.conn.commit()
                    self.logger.log_activity(f"Updated {field_name} for user {user_id} in {table_name}", "Successful")

                    # Update the selected_user tuple to reflect the changes
                    selected_user = list(selected_user)
                    
                    # Update the correct index in the list based on field_choice
                    if field_choice == '1':
                        selected_user[1] = new_value  # Encrypted username
                    elif field_choice == '2':
                        selected_user[3] = new_value  # First name
                    elif field_choice == '3':
                        selected_user[4] = new_value  # Last name
                    elif field_choice == '4':
                        selected_user[5] = new_value  # Registration date
                    elif field_choice == '5':
                        selected_user[6] = new_value  # Role
                    
                    selected_user = tuple(selected_user)

                    print(f"{field_name.capitalize()} updated to: {new_value}")
                    field_updated = True
            else:
                print("Invalid choice. Please enter a number from the menu.")

        if field_updated:
            if input("Do you want to edit anything else for this user? (yes/no): ").strip().lower() != 'yes':
                return
