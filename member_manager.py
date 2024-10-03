# member_manager.py
import os
from datetime import datetime
import input_checker as ic
import sqlite3

class MemberManager:

    def __init__(self, log_manager):
        self.conn = sqlite3.connect('unique_meal.db')
        self.cursor = self.conn.cursor()
        self.cities = ["Amsterdam", "Rotterdam", "Utrecht", "The Hague", "Eindhoven", "Groningen", "Maastricht", "Leiden", "Delft", "Breda"]
        self.log_manager = log_manager
        self.cities = ["Amsterdam", "Rotterdam", "Utrecht", "The Hague", "Eindhoven", "Groningen", "Maastricht", "Leiden", "Delft", "Breda"]

    def register_member(self):
        member_id = self.generate_membership_id()
        firstname = ic.validate_fname_or_lname_input("Enter first name: ")
        lastname = ic.validate_fname_or_lname_input("Enter last name: ")
        age = ic.get_valid_int_input("Enter age: ")
        gender = ic.get_valid_gender_input("Enter gender (M/F): ")
        weight = ic.get_valid_int_input("Enter weight: ")
        address = self.address_input()
        email = ic.get_valid_email_input("Enter email: ")
        phone = ic.get_valid_phone_input("Enter phone (8 digits): ")

        sql = 'INSERT INTO members (member_id, firstname, lastname, gender, age, weight, address, email, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        try:
            self.cursor.execute(sql, (member_id, firstname, lastname, gender, age, weight, address, email, phone))
            self.conn.commit()
            print(f"Member {firstname} {lastname} registered successfully. Member ID: {member_id}")
            self.log_manager.log_activity(f"Registered member {firstname} {lastname}", "Successful")
        except sqlite3.IntegrityError:
            print("Error: Member already exists.")
            self.log_manager.log_activity("Failed to register member {firstname} {lastname}", "IntegrityError")

    def address_input(self):
        street_name = input("Enter street name: ")
        house_number = ic.get_valid_int_input("Enter house number: ")
        zip_code = ic.get_valid_zip_code_input("Enter zip code (DDDDXX): ")

        # Display predefined city list
        print("Select a city from the following list:")
        for index, city in enumerate(self.cities, start=1):
            print(f"{index}. {city}")

        city = ic.get_valid_city_input("Enter the number corresponding to the city: ")
        address = f"{street_name}, {house_number}, {zip_code}, {city}"
        return address

    def generate_membership_id(self):
        year = str(datetime.now().year)[2:]
        random_digits = ''.join([str(os.urandom(1)[0] % 10) for _ in range(7)])
        partial_id = year + random_digits
        checksum = sum(int(digit) for digit in partial_id) % 10
        membership_id = partial_id + str(checksum)
        return membership_id
    
    def search_members_querry(self, search_key):
        search_key = f"%{search_key}%"
        sql = '''SELECT member_id, firstname, lastname, age, gender, weight, address, email, phone 
                 FROM members 
                 WHERE member_id LIKE ? 
                 OR firstname LIKE ? 
                 OR lastname LIKE ? 
                 OR age LIKE ?
                 OR gender LIKE ?
                 OR weight LIKE ?
                 OR address LIKE ? 
                 OR email LIKE ? 
                 OR phone LIKE ?'''
        self.cursor.execute(sql, (search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key, search_key))
        results = self.cursor.fetchall()
        self.conn.commit()
        return results
    
    def search_members(self, search_key1):
        results = self.search_members_querry(search_key1)
        if results:
            print("Search Results:")
            for row in results:
                member_id, firstname, lastname, age, gender, weight, address, email, phone = row
                print(f"ID: {member_id}, Name: {firstname} {lastname}, Age: {age}, Gender: {gender}, Weight: {weight}")
                print(f"Address: {address}")
                print(f"Email: {email}, Phone: {phone}")
                print("-" * 20)
        else:
            print("No matching members found.")
            
        input("Press any key to continue...")
        os.system('cls' if os.name == 'nt' else 'clear') 

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def fetch_members(self):
        sql_select = 'SELECT * FROM members'
        self.cursor.execute(sql_select)
        members = self.cursor.fetchall()
        self.conn.commit()
        return members  
    
    def edit_member(self):
            while True:
                self.clear_console()

                search_key = input("Enter search keyword (member ID, first name, last name, etc.): ").strip()
                results = self.search_members_querry(search_key)

                if len(results) > 10:
                    print("More than 10 members found. Please refine your search.")
                elif len(results) == 0:
                    print("No matching members found.")
                else:
                    selected_member = self.select_member_from_results(results)
                    if selected_member:
                        self.edit_member_details(selected_member)

                if input("Do you want to edit anything else? (yes/no): ").strip().lower() != 'yes':
                    break

    def remove_member(self):
        while True:
            self.clear_console()

            search_key = input("Enter search keyword (member ID, first name, last name, etc.): ").strip()
            results = self.search_members_querry(search_key)

            if len(results) > 10:
                print("More than 10 members found. Please refine your search.")
            elif len(results) == 0:
                print("No matching members found.")
            else:
                selected_member = self.select_member_from_results(results)
                if selected_member:
                    self.delete_member(selected_member[0])

            if input("Do you want to remove another member? (yes/no): ").strip().lower() != 'yes':
                break

    def select_member_from_results(self, results):
        while True:
            try:
                self.clear_console()
                print("Search Results:")
                for index, row in enumerate(results, start=1):
                    member_id, firstname, lastname, age, gender, weight, address, email, phone = row
                    print(f"{index}. ID: {member_id}, Name: {firstname} {lastname}")

                choice = int(input("Enter the number of the member to select (or '0' to cancel): ").strip())
                if choice == 0:
                    print("Canceled.")
                    return None
                elif 1 <= choice <= len(results):
                    return results[choice - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def edit_member_details(self, selected_member):
        member_id = selected_member[0]
        field_updated = False

        while True:
            self.clear_console()
            print(f"Editing member ID {member_id}:")
            print("-----------------------------")
            print(f"1. First Name: {selected_member[1]}")
            print(f"2. Last Name: {selected_member[2]}")
            print(f"3. Age: {selected_member[3]}")
            print(f"4. Gender: {selected_member[4]}")
            print(f"5. Weight: {selected_member[5]}")
            print(f"6. Address: {selected_member[6]}")
            print(f"7. Email: {selected_member[7]}")
            if len(selected_member) > 8:
                print(f"8. Phone: {selected_member[8]}")
            print("-----------------------------")

            field_choice = input("Enter the number of the field to edit (or '0' to finish editing this member): ").strip()

            if field_choice == '0':
                print("Finished editing this member.")
                break
            elif field_choice in {'1', '2', '3', '4', '5', '6', '7', '8'}:
                new_value = None
                field_name = None
                if field_choice == '1':
                    new_value = ic.validate_fname_or_lname_input("Enter new first name: ")
                    field_name = 'firstname'
                elif field_choice == '2':
                    new_value = ic.validate_fname_or_lname_input("Enter new last name: ")
                    field_name = 'lastname'
                elif field_choice == '3':
                    new_value = ic.get_valid_int_input("Enter new age: ")
                    field_name = 'age'
                elif field_choice == '4':
                    new_value = ic.get_valid_gender_input("Enter new gender: ")
                    field_name = 'gender'
                elif field_choice == '5':
                    new_value = ic.get_valid_int_input("Enter new weight: ")
                    field_name = 'weight'
                elif field_choice == '6':
                    new_value = input("Enter new address: ").strip()
                    field_name = 'address'
                elif field_choice == '7':
                    new_value = ic.get_valid_email_input("Enter new email: ")
                    field_name = 'email'
                elif field_choice == '8':
                    new_value = ic.get_valid_phone_input("Enter new phone number: ")
                    field_name = 'phone'

                if new_value is not None and field_name is not None:
                    sql_update = f'UPDATE members SET {field_name} = ? WHERE member_id = ?'
                    self.cursor.execute(sql_update, (new_value, member_id))
                    self.conn.commit()
                    self.log_manager.log_activity(f"Updated {field_name} for member {member_id}", "Successful")

                    selected_member = list(selected_member)
                    field_choice = int(field_choice) 
                    selected_member[field_choice] = new_value
                    selected_member = tuple(selected_member)

                    print(f"{field_name.capitalize()} updated to: {new_value}")
                    field_updated = True
            else:
                print("Invalid choice. Please enter a number from the menu.")

        if field_updated:
            if input("Do you want to edit anything else for this member? (yes/no): ").strip().lower() != 'yes':
                return

    def delete_member(self, member_id):
        confirmation = input(f"Are you sure you want to delete member ID {member_id}? (yes/no): ").strip().lower()
        if confirmation == 'yes':
            sql_delete = 'DELETE FROM members WHERE member_id = ?'
            self.cursor.execute(sql_delete, (member_id,))
            self.conn.commit()
            self.log_manager.log_activity(f"Deleted member ID {member_id}", "Successful")
            print(f"Member ID {member_id} deleted.")
        else:
            print("Deletion canceled.")

    def close(self):
        self.conn.close()