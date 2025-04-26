#!/usr/bin/python
import psycopg2
import csv
import sys
from config import config

def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server, returns a connection object
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting to database: {error}")
        sys.exit(1)

def upload_from_csv(file_path):
    """Upload data from CSV file"""
    conn = None
    try:
        conn = connect()
        with conn.cursor() as cursor:
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    cursor.execute(
                        "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                        (row['first_name'], row['last_name'], row['phone_number'])
                    )
            conn.commit()
            print(f"Data from {file_path} uploaded successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error uploading data: {error}")
    finally:
        if conn is not None:
            conn.close()

def add_contact_from_console():
    """Add a new contact from console input"""
    conn = None
    try:
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        phone_number = input("Enter phone number: ")
        
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO contacts (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                (first_name, last_name, phone_number)
            )
        conn.commit()
        print(f"Contact {first_name} {last_name} added successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error adding contact: {error}")
    finally:
        if conn is not None:
            conn.close()

def update_contact():
    """Update contact information"""
    conn = None
    try:
        first_name = input("Enter first name of contact to update: ")
        last_name = input("Enter last name of contact to update: ")
        
        choice = input("What would you like to update? (1 - First Name, 2 - Last Name, 3 - Phone Number): ")
        
        conn = connect()
        with conn.cursor() as cursor:
            if choice == '1':
                new_first_name = input("Enter new first name: ")
                cursor.execute(
                    "UPDATE contacts SET first_name = %s WHERE first_name = %s AND last_name = %s",
                    (new_first_name, first_name, last_name)
                )
            elif choice == '2':
                new_last_name = input("Enter new last name: ")
                cursor.execute(
                    "UPDATE contacts SET last_name = %s WHERE first_name = %s AND last_name = %s",
                    (new_last_name, first_name, last_name)
                )
            elif choice == '3':
                new_phone = input("Enter new phone number: ")
                cursor.execute(
                    "UPDATE contacts SET phone_number = %s WHERE first_name = %s AND last_name = %s",
                    (new_phone, first_name, last_name)
                )
            else:
                print("Invalid choice")
                return
                
        rows_updated = cursor.rowcount
        conn.commit()
        
        if rows_updated > 0:
            print("Contact updated successfully")
        else:
            print(f"No contact found with name {first_name} {last_name}")
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating contact: {error}")
    finally:
        if conn is not None:
            conn.close()

def query_contacts():
    """Query contacts with different filters"""
    conn = None
    try:
        print("Select filter type:")
        print("1. By first name")
        print("2. By last name")
        print("3. By phone number")
        print("4. Show all contacts")
        
        choice = input("Enter your choice (1-4): ")
        
        conn = connect()
        with conn.cursor() as cursor:
            if choice == '1':
                name = input("Enter first name: ")
                cursor.execute("SELECT * FROM contacts WHERE first_name = %s", (name,))
            elif choice == '2':
                name = input("Enter last name: ")
                cursor.execute("SELECT * FROM contacts WHERE last_name = %s", (name,))
            elif choice == '3':
                phone = input("Enter phone number: ")
                cursor.execute("SELECT * FROM contacts WHERE phone_number = %s", (phone,))
            elif choice == '4':
                cursor.execute("SELECT * FROM contacts")
            else:
                print("Invalid choice")
                return
                
            rows = cursor.fetchall()
            
            if rows:
                print("\nContacts found:")
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Created: {row[4]}")
            else:
                print("No contacts found")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error querying contacts: {error}")
    finally:
        if conn is not None:
            conn.close()

def delete_contact():
    """Delete contact by username or phone"""
    conn = None
    try:
        print("Delete by:")
        print("1. First name")
        print("2. Last name")
        print("3. Phone number")
        
        choice = input("Enter your choice (1-3): ")
        
        conn = connect()
        with conn.cursor() as cursor:
            if choice == '1':
                name = input("Enter first name: ")
                cursor.execute("DELETE FROM contacts WHERE first_name = %s", (name,))
            elif choice == '2':
                name = input("Enter last name: ")
                cursor.execute("DELETE FROM contacts WHERE last_name = %s", (name,))
            elif choice == '3':
                phone = input("Enter phone number: ")
                cursor.execute("DELETE FROM contacts WHERE phone_number = %s", (phone,))
            else:
                print("Invalid choice")
                return
                
            rows_deleted = cursor.rowcount
            conn.commit()
            
            if rows_deleted > 0:
                print(f"{rows_deleted} contact(s) deleted successfully")
            else:
                print("No contacts found to delete")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting contact: {error}")
    finally:
        if conn is not None:
            conn.close()

def search_pattern():
    """Search contacts based on a pattern"""
    conn = None
    try:
        pattern = input("Enter search pattern (part of name, surname, or phone): ")
        pattern = f"%{pattern}%"  # Add wildcards for partial matching
        
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM contacts 
                WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone_number ILIKE %s
                """, 
                (pattern, pattern, pattern)
            )
            
            rows = cursor.fetchall()
            
            if rows:
                print("\nContacts found:")
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Created: {row[4]}")
            else:
                print("No contacts found matching the pattern")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error searching contacts: {error}")
    finally:
        if conn is not None:
            conn.close()

def insert_or_update_contact():
    """Insert new user by name and phone, update phone if user already exists"""
    conn = None
    try:
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        phone_number = input("Enter phone number: ")
        
        conn = connect()
        with conn.cursor() as cursor:
            # Call the stored procedure
            cursor.execute(
                "CALL insert_or_update_contact(%s, %s, %s)",
                (first_name, last_name, phone_number)
            )
        conn.commit()
        print(f"Contact {first_name} {last_name} inserted or updated successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error with contact: {error}")
    finally:
        if conn is not None:
            conn.close()

def insert_multiple_contacts():
    """Insert multiple contacts using stored procedure"""
    conn = None
    try:
        num_contacts = int(input("How many contacts do you want to add? "))
        contacts = []
        
        for i in range(num_contacts):
            print(f"\nEnter details for contact {i+1}:")
            first_name = input("First name: ")
            last_name = input("Last name: ")
            phone_number = input("Phone number: ")
            contacts.append([first_name, last_name, phone_number])
        
        conn = connect()
        with conn.cursor() as cursor:
            # Convert Python list to PostgreSQL array format
            cursor.execute(
                "CALL insert_multiple_contacts(%s::text[][])",
                (contacts,)
            )
        conn.commit()
        print("Contacts processed")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error with contacts: {error}")
    finally:
        if conn is not None:
            conn.close()

def query_paginated():
    """Query contacts with pagination"""
    conn = None
    try:
        limit = int(input("Enter number of records per page: "))
        offset = int(input("Enter offset (starting from 0): "))
        
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM get_contacts_paginated(%s, %s)",
                (limit, offset)
            )
            
            rows = cursor.fetchall()
            
            if rows:
                print(f"\nContacts (page with limit {limit}, offset {offset}):")
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]} {row[2]}, Phone: {row[3]}, Created: {row[4]}")
            else:
                print("No contacts found on this page")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error querying contacts: {error}")
    finally:
        if conn is not None:
            conn.close()

def delete_by_procedure():
    """Delete contact by username or phone using procedure"""
    conn = None
    try:
        print("Delete by:")
        print("1. Name (first or last)")
        print("2. Phone number")
        
        choice = input("Enter your choice (1-2): ")
        
        if choice == '1':
            identifier = input("Enter name: ")
            type_value = "name"
        elif choice == '2':
            identifier = input("Enter phone number: ")
            type_value = "phone"
        else:
            print("Invalid choice")
            return
            
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute(
                "CALL delete_contact(%s, %s)",
                (identifier, type_value)
            )
        conn.commit()
        print("Operation completed")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting contact: {error}")
    finally:
        if conn is not None:
            conn.close()

def main():
    """Main function with menu"""
    while True:
        print("\n===== PhoneBook Management System =====")
        print("1. Upload contacts from CSV file")
        print("2. Add new contact")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Search contacts by pattern")
        print("7. Insert or update contact (procedure)")
        print("8. Insert multiple contacts (procedure)")
        print("9. Query contacts with pagination")
        print("10. Delete contact using procedure")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            file_path = input("Enter CSV file path (default: phonebook.csv): ") or "phonebook.csv"
            upload_from_csv(file_path)
        elif choice == '2':
            add_contact_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            search_pattern()
        elif choice == '7':
            insert_or_update_contact()
        elif choice == '8':
            insert_multiple_contacts()
        elif choice == '9':
            query_paginated()
        elif choice == '10':
            delete_by_procedure()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()