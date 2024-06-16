from systemadmin_manager import SystemAdminManager
import os
from datetime import datetime
import input_checker as ic
from BaseUsers import BaseUsers
import sqlite3

class SuperAdminManager(SystemAdminManager):
    def __init__(self, log_manager):
        super().__init__(log_manager)

    def search_sa_querry(self, search_key):
            search_key = f"%{search_key}%"
            sql = '''SELECT * FROM system_admins WHERE username LIKE ? 
                    OR first_name LIKE ? OR last_name LIKE ? 
                    OR registration_date LIKE ? OR role LIKE ?'''
            self.cursor.execute(sql, (search_key, search_key, search_key, search_key, search_key))
            results = self.cursor.fetchall()
            return results

    def search_sa(self, search_key):
        results = self.search_sa_querry(search_key)
        if results:
            print("Search Results:")
            for result in results:
                sa_id, username, firstname, lastname, registration_date, role = result
                print(f"System Admin ID: {sa_id}")
                print(f"Username: {username}")
                print(f"Name: {firstname} {lastname}")
                print(f"Registration Date: {registration_date}")
                print(f"Role: {role}")
                print("-" * 20)
        else:
            print("No matching system admins found.")

