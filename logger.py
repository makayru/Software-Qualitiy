# logger.py
import sqlite3
import datetime
from encryption import RSAEncryption
import os
import Display as display

class LoggerDatabaseManager:
    def __init__(self, db_name='logs.db'):
        self.db_name = db_name
        self.init_db()
        self.current_user = None
        self.current_role = None
        self.encryption = RSAEncryption()

    def set_current_user(self, username, role):
        self.clear_console()
        self.current_user = username
        self.current_role = role
        if self.current_role in ["Super_Administrator", "SystemAdmin"]:
            self.alert_unread_suspicious_logs()
            input("Press Enter to continue...")


    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date TEXT,
                        time TEXT,
                        username TEXT,
                        activity TEXT,
                        additional_info TEXT,
                        suspicious TEXT,
                        read TEXT DEFAULT 'unread')''')
        conn.commit()
        conn.close()

    def log_activity(self, activity, additional_info='', suspicious='No'):
        username = self.current_user
        now = datetime.datetime.now()
        query = '''INSERT INTO logs (date, time, username, activity, additional_info, suspicious, read) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)'''
        
        read_status = 'unread' if suspicious == 'Yes' else 'read'

        enc_date = self.encryption.encrypt_data(now.strftime("%Y-%m-%d"))
        enc_time = self.encryption.encrypt_data(now.strftime("%H:%M:%S"))
        enc_username = self.encryption.encrypt_data(username)
        enc_activity = self.encryption.encrypt_data(activity)
        enc_additional_info = self.encryption.encrypt_data(additional_info)
        enc_suspicious = self.encryption.encrypt_data(suspicious)
        enc_read_status = self.encryption.encrypt_data(read_status)
        

        params = (enc_date, enc_time, enc_username, enc_activity, enc_additional_info, enc_suspicious, enc_read_status)
        self.execute_query(query, params)

    def execute_query(self, query, params):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
        conn.close()

    def is_suspicious_activity(self, username, activity):
        # Example criteria for suspicion
        if activity == 'login attempt' and self.check_failed_logins(username) > 5:
            return 'Yes'
        if activity == 'data access' and self.access_volume(username) > 1000:
            return 'Yes'
        if self.is_blacklisted_ip(self.get_user_ip(username)):
            return 'Yes'
        if self.is_out_of_normal_hours():
            return 'Yes'
        return 'No'

    def access_volume(self, username):
        # Mock function to check the volume of accessed data
        return 1200  # Example: return a number greater than the threshold

    def is_blacklisted_ip(self, ip):
        # Mock function to check if the IP is blacklisted
        blacklisted_ips = ['192.168.1.1', '10.0.0.1']
        return ip in blacklisted_ips

    def get_user_ip(self, username):
        # Mock function to get the user's IP address
        return '192.168.1.1'  # Example: return a blacklisted IP
    
    def is_out_of_normal_hours(self):
        # Mock function to check if the current time is outside normal hours
        current_hour = datetime.datetime.now().hour
        return current_hour < 6 or current_hour > 18

    def get_unread_suspicious_logs(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute ( "SELECT * FROM logs")
        all_logs = c.fetchall()
        conn.close()
        
        unread_suspicious_logs = []
        for log in all_logs:
            decrypted_id = log[0] 
            decrypted_date = self.encryption.decrypt_data(log[1])
            decrypted_time = self.encryption.decrypt_data(log[2])
            decrypted_user = self.encryption.decrypt_data(log[3])
            decrypted_activity = self.encryption.decrypt_data(log[4])
            decrypted_info = self.encryption.decrypt_data(log[5])
            decrypted_suspicious = self.encryption.decrypt_data(log[6])
            decrypted_read = self.encryption.decrypt_data(log[7])
            
            if decrypted_suspicious == 'Yes' and decrypted_read == 'unread':
                unread_suspicious_logs.append({
                    'id': decrypted_id,
                    'date': decrypted_date,
                    'time': decrypted_time,
                    'user': decrypted_user,
                    'activity': decrypted_activity,
                    'additional_info': decrypted_info,
                    'suspicious': decrypted_suspicious,
                    'read': decrypted_read
                })
        
        return unread_suspicious_logs

    def mark_logs_as_read(self):
        query = "UPDATE logs SET read=? "

        enc_read = self.encryption.encrypt_data('read')

        self.execute_query(query, (enc_read,))

    def alert_unread_suspicious_logs(self):
        """Alert the admin about unread suspicious logs."""
        unread_logs = self.get_unread_suspicious_logs()
        if unread_logs:
            print(f"\n{'='*50}")
            print(f"ALERT: You have {len(unread_logs)} unread suspicious activities!")
            print(f"{'='*50}\n")
            print(f"{'ID':<5} {'Date':<15} {'Time':<10} {'User':<15} {'Activity':<30} {'Additional Info':<50}")
            print('-' * 115)  # Underline for the header

            for log in unread_logs:
                print(f"{log['id']:<5} {log['date']:<15} {log['time']:<10} {log['user']:<15} {log['activity']:<30} {log['additional_info']:<30}")
            
            self.mark_logs_as_read()  # Mark them as read after the admin views them
        else:
            print("No unread suspicious activities found.")


    def view_logs(self, page=0, limit=10):
        a = True
        while a == True:
            self.clear_console()
            offset = page * limit 
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM logs LIMIT ? OFFSET ?", (limit, offset))
            logs = cursor.fetchall()
            conn.close()

            if not logs:
                print("No more logs to display.")
                return
            
            for log in logs:
                decrypted_id = log[0] 
                decrypted_date = self.encryption.decrypt_data(log[1])
                decrypted_time = self.encryption.decrypt_data(log[2])
                decrypted_user = self.encryption.decrypt_data(log[3])
                decrypted_activity = self.encryption.decrypt_data(log[4])
                decrypted_info = self.encryption.decrypt_data(log[5])
                decrypted_suspicious = self.encryption.decrypt_data(log[6])
                decrypted_read = self.encryption.decrypt_data(log[7])

                print(f"Log ID: {decrypted_id}, Date: {decrypted_date}, Time: {decrypted_time}, User: {decrypted_user}")
                print(f"Activity: {decrypted_activity}, Additional Info: {decrypted_info}, Suspicious: {decrypted_suspicious}, Read: {decrypted_read}")


            print("\nControls:")
            print("Press 'n' for next 10 logs.")
            print("Press 'p' for previous 10 logs.")
            print("Press 'q' to quit.")

            user_input = input("Enter command: ").strip().lower()
            
            if user_input == 'n':
                page+=1  # Load the next page
            elif user_input == 'p' and page > 0:
                page -= 1  # Load the previous page
            elif user_input == 'q':
                print("Exiting log viewer.")
                a = False
            else:
                print("Invalid command. Please try again.")

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')