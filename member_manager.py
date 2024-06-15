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
        firstname = input("Enter first name: ")
        lastname = input("Enter last name: ")
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


