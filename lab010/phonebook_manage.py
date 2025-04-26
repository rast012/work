import psycopg2
import csv
import os
import json # For potentially handling structured input/output if needed
from config import config # Import the config function from config.py

def connect():
    #Connect to the PostgreSQL database server 
    conn = None
    try:
        # Read connection parameters
        params = config()
        if params is None:
            print("Database configuration could not be loaded. Exiting.")
            return None

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connection successful.')

        # Create table if it doesn't exist upon first connection
        create_table(conn)

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting to database: {error}")
        if conn is not None:
            conn.close() # Ensure connection is closed on error
        return None

def create_table(conn):
    #Create the contacts table if it doesn't exist
    command = """
        CREATE TABLE IF NOT EXISTS contacts (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR(255) NOT NULL,
            last_name VARCHAR(255),
            phone VARCHAR(50) NOT NULL UNIQUE
        )
        """
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
        # print("Table 'contacts' checked/created successfully.") # Optional: less verbose
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
        conn.rollback() # Rollback if table creation fails
        if cur:
            cur.close()
        # Re-raise or handle appropriately if connection should fail
        raise error # Or return False/None

# --- Helper Functions ---

def display_results(rows, description):
    """ Helper function to display query results neatly """
    if not rows:
        print("\n--- No records found ---")
        return

    print("\n--- Query Results ---")
    if not description:
        # Handle cases where description might be missing (though unlikely with SELECT *)
        print("[No column names available]")
        for row in rows:
            print(row)
        return

    # Print header
    headers = [col.name for col in description]
    print(f"{' | '.join(headers)}")
    # Dynamic separator based on typical content width or header width
    col_widths = [max(len(h), 15) for h in headers] # Min width 15 for data
    print("-" * (sum(col_widths) + (len(headers) * 3) - 1))

    # Print rows
    for row in rows:
        formatted_row = []
        for i, item in enumerate(row):
            # Basic formatting: truncate long strings if needed, align left
            s_item = str(item) if item is not None else ''
            formatted_row.append(s_item.ljust(col_widths[i]))
        print(f"{' | '.join(formatted_row)}")

    print("-" * (sum(col_widths) + (len(headers) * 3) - 1))
    print(f"Total records: {len(rows)}")


# --- Core Functionality (Implemented in Python) ---

def insert_from_csv(conn, csv_filepath='contacts.csv'):
    """ Insert multiple contacts from a CSV file using ON CONFLICT """
    script_dir = os.path.dirname(__file__)
    abs_csv_path = os.path.join(script_dir, csv_filepath)

    if not os.path.exists(abs_csv_path):
        print(f"Error: CSV file '{abs_csv_path}' not found.")
        return

    # Use ON CONFLICT (phone) DO NOTHING to avoid duplicates based on phone
    sql = """
        INSERT INTO contacts(first_name, last_name, phone)
        VALUES(%s, %s, %s)
        ON CONFLICT (phone) DO NOTHING
        """
    cur = None
    inserted_count = 0
    skipped_count = 0
    error_count = 0

    try:
        cur = conn.cursor()
        with open(abs_csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader) # Skip header row
            print(f"\nReading data from {abs_csv_path}...")
            for i, row in enumerate(reader):
                if len(row) == 3:
                    first_name, last_name, phone = row[0].strip(), row[1].strip(), row[2].strip()
                    if not first_name or not phone:
                         print(f"Skipping row {i+1}: Missing first name or phone.")
                         skipped_count += 1
                         continue
                    try:
                        cur.execute(sql, (first_name, last_name if last_name else None, phone))
                        if cur.rowcount > 0:
                            inserted_count += 1
                        else:
                            # This means ON CONFLICT clause was triggered or no actual insert happened
                            # print(f"Skipped duplicate or existing phone: {phone}") # Optional: Can be verbose
                            skipped_count += 1
                    except (Exception, psycopg2.DatabaseError) as insert_error:
                        print(f"Error inserting row {i+1} ({row}): {insert_error}")
                        conn.rollback() # Rollback the single failed statement's effect if needed
                        error_count += 1
                        # Decide whether to continue or stop on error
                        # continue
                else:
                     print(f"Skipping invalid row {i+1} (expected 3 columns): {row}")
                     skipped_count += 1

        conn.commit() # Commit all successful inserts at the end
        print(f"\nCSV import complete.")
        print(f"  Inserted: {inserted_count}")
        print(f"  Skipped (duplicates/missing data): {skipped_count}")
        print(f"  Errors: {error_count}")


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError during CSV import process: {error}")
        conn.rollback() # Rollback transaction on error
    finally:
        if cur:
            cur.close()

def insert_from_console(conn):
    """ Insert a single new contact from console input """
    # Using ON CONFLICT to handle potential duplicate phone numbers gracefully
    sql = """
        INSERT INTO contacts(first_name, last_name, phone)
        VALUES(%s, %s, %s)
        ON CONFLICT (phone) DO NOTHING
        RETURNING contact_id;
        """
    cur = None
    try:
        print("\n--- Insert New Contact ---")
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name (optional): ").strip()
        phone = input("Enter phone number: ").strip()

        if not first_name or not phone:
            print("Error: First name and phone number cannot be empty.")
            return

        cur = conn.cursor()
        cur.execute(sql, (first_name, last_name if last_name else None, phone))
        result = cur.fetchone()

        if result:
            contact_id = result[0]
            conn.commit()
            print(f"Contact inserted successfully with ID: {contact_id}")
        else:
            # This means ON CONFLICT happened
            conn.rollback() # No changes were made, so rollback (or just don't commit)
            print(f"Contact with phone number '{phone}' already exists. Insertion skipped.")


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting contact: {error}")
        conn.rollback() # Rollback transaction on error
    finally:
        if cur:
            cur.close()

def update_contact(conn):
    """ Update an existing contact's first name or phone number """
    cur = None
    print("\n--- Update Contact ---")
    try:
        identifier = input("Enter contact ID or current phone number of the contact to update: ").strip()
        if not identifier:
            print("Identifier cannot be empty.")
            return

        print("Which field to update?")
        print(" 1. First Name")
        print(" 2. Last Name")
        print(" 3. Phone Number")
        field_choice = input("Enter choice (1-3): ").strip()

        field_to_update = None
        if field_choice == '1':
            field_to_update = 'first_name'
        elif field_choice == '2':
            field_to_update = 'last_name'
        elif field_choice == '3':
            field_to_update = 'phone'
        else:
            print("Invalid choice.")
            return

        new_value = input(f"Enter the new value for {field_to_update}: ").strip()
        if field_to_update in ['first_name', 'phone'] and not new_value:
             print(f"New value for {field_to_update} cannot be empty.")
             return
        # Allow empty last name

        cur = conn.cursor()
        updated_rows = 0

        # Determine if identifier is ID (numeric) or phone (string)
        try:
            contact_id = int(identifier)
            # Update by ID
            sql = f"UPDATE contacts SET {field_to_update} = %s WHERE contact_id = %s"
            cur.execute(sql, (new_value if new_value else None, contact_id))
        except ValueError:
            # Update by Phone
            sql = f"UPDATE contacts SET {field_to_update} = %s WHERE phone = %s"
            cur.execute(sql, (new_value if new_value else None, identifier))

        updated_rows = cur.rowcount

        if updated_rows > 0:
            conn.commit()
            print(f"Contact updated successfully. {updated_rows} row(s) affected.")
        else:
            print("Contact not found with the specified ID or phone number, or no changes made.")
            conn.rollback() # No need to commit if nothing changed

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating contact: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def query_contacts_by_pattern(conn):
    """ Query contacts where pattern matches part of first name, last name, or phone """
    cur = None
    print("\n--- Search Contacts by Pattern ---")
    try:
        pattern = input("Enter search pattern (part of name or phone): ").strip()
        if not pattern:
            print("Search pattern cannot be empty.")
            return

        sql = """
            SELECT contact_id, first_name, last_name, phone
            FROM contacts
            WHERE first_name ILIKE %s
               OR last_name ILIKE %s
               OR phone ILIKE %s
            ORDER BY first_name, last_name;
            """
        search_term = f'%{pattern}%' # Add wildcards for partial matching

        cur = conn.cursor()
        cur.execute(sql, (search_term, search_term, search_term))
        rows = cur.fetchall()
        display_results(rows, cur.description)

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error querying contacts by pattern: {error}")
    finally:
        if cur:
            cur.close() # Close cursor even on error

def upsert_contact(conn):
    """ Insert a new contact or update existing one based on phone number """
    # This uses INSERT ... ON CONFLICT ... DO UPDATE
    sql = """
        INSERT INTO contacts (first_name, last_name, phone)
        VALUES (%s, %s, %s)
        ON CONFLICT (phone) DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name
        RETURNING contact_id, (xmax = 0) AS inserted;
        -- xmax = 0 indicates an INSERT occurred, otherwise it was an UPDATE
    """
    cur = None
    print("\n--- Add or Update Contact (Upsert) ---")
    try:
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name (optional): ").strip()
        phone = input("Enter phone number: ").strip()

        if not first_name or not phone:
            print("Error: First name and phone number cannot be empty.")
            return

        cur = conn.cursor()
        cur.execute(sql, (first_name, last_name if last_name else None, phone))
        contact_id, was_inserted = cur.fetchone()
        conn.commit()

        if was_inserted:
            print(f"Contact inserted successfully with ID: {contact_id}")
        else:
            print(f"Contact with phone '{phone}' updated successfully (ID: {contact_id}).")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error during upsert operation: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()

def bulk_insert_validated(conn):
    """ Insert multiple contacts from console input, with basic validation """
    contacts_list = []
    invalid_entries = []
    print("\n--- Bulk Insert Contacts (Enter blank first name to finish) ---")
    while True:
        first_name = input("  Enter first name: ").strip()
        if not first_name:
            break
        last_name = input("  Enter last name (optional): ").strip()
        phone = input("  Enter phone number: ").strip()

        # Basic Python Validation
        contact_info = {"first_name": first_name, "last_name": last_name, "phone": phone}
        is_valid = True
        reason = ""
        if not phone:
            is_valid = False
            reason = "Phone number is required."
        # Add more validation if needed (e.g., simple phone format check)
        # elif not re.match(r'^[0-9()+\-\s]+$', phone): # Example regex
        #     is_valid = False
        #     reason = "Invalid phone format (only digits, (), +, -, space allowed)."

        if is_valid:
            contacts_list.append(contact_info)
        else:
            contact_info["reason"] = reason
            invalid_entries.append(contact_info)
            print(f"  -> Invalid entry skipped: {reason}")


    if not contacts_list:
        print("\nNo valid contacts entered for bulk insert.")
        if invalid_entries:
             print("\n--- Skipped Invalid Entries ---")
             for entry in invalid_entries:
                 print(f"  {entry}")
        return

    # Use ON CONFLICT (phone) DO NOTHING for bulk insert
    sql = """
        INSERT INTO contacts(first_name, last_name, phone)
        VALUES(%s, %s, %s)
        ON CONFLICT (phone) DO NOTHING
        """
    cur = None
    inserted_count = 0
    skipped_due_to_conflict = 0
    error_count = 0

    try:
        cur = conn.cursor()
        print(f"\nAttempting to insert {len(contacts_list)} valid contacts...")
        for contact in contacts_list:
            try:
                cur.execute(sql, (
                    contact['first_name'],
                    contact['last_name'] if contact['last_name'] else None,
                    contact['phone']
                ))
                if cur.rowcount > 0:
                    inserted_count += 1
                else:
                    skipped_due_to_conflict += 1
            except (Exception, psycopg2.DatabaseError) as insert_error:
                print(f"  Error inserting contact {contact}: {insert_error}")
                conn.rollback() # Rollback this specific error if desired
                error_count += 1
                invalid_entries.append({"reason": str(insert_error), "contact": contact})
                # continue # Continue with the next contact

        conn.commit() # Commit all successful inserts
        print("\nBulk insert process finished.")
        print(f"  Successfully Inserted: {inserted_count}")
        print(f"  Skipped (Existing Phone): {skipped_due_to_conflict}")
        print(f"  Errors during insert: {error_count}")

        if invalid_entries:
            print("\n--- Invalid/Skipped/Error Entries ---")
            # Use json dumps for potentially better formatting if needed
            # print(json.dumps(invalid_entries, indent=2))
            for entry in invalid_entries:
                 print(f"  Reason: {entry.get('reason', 'Validation failed')} | Data: {entry}")


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"\nError during bulk insert transaction: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()


def query_contacts_paginated(conn):
    """ Query contacts with limit and offset for pagination """
    cur = None
    print("\n--- Query Contacts (by page) ---")
    try:
        limit_str = input("Enter limit (number of records per page, e.g., 10): ").strip()
        offset_str = input("Enter offset (number of records to skip, e.g., 0): ").strip()

        limit = int(limit_str)
        offset = int(offset_str)

        if limit <= 0 or offset < 0:
            print("Limit must be positive, and offset must be non-negative.")
            return

        sql = """
            SELECT contact_id, first_name, last_name, phone
            FROM contacts
            ORDER BY contact_id -- Or first_name, last_name
            LIMIT %s
            OFFSET %s;
            """

        cur = conn.cursor()
        cur.execute(sql, (limit, offset))
        rows = cur.fetchall()
        display_results(rows, cur.description)

    except ValueError:
        print("Invalid input. Limit and offset must be integers.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error querying contacts with pagination: {error}")
    finally:
        if cur:
            cur.close()

def delete_contact(conn):
    """ Delete a contact by ID, phone number, or name (first/last) """
    cur = None
    print("\n--- Delete Contact ---")
    try:
        identifier = input("Enter contact ID, phone number, first name, or last name to delete: ").strip()
        if not identifier:
            print("Identifier cannot be empty.")
            return

        confirm = input(f"WARNING: If using a name, this might delete MULTIPLE contacts.\nAre you sure you want to delete contacts matching '{identifier}'? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return

        cur = conn.cursor()
        deleted_rows = 0

        # Try deleting by ID first if it's an integer
        try:
            contact_id = int(identifier)
            sql_id = "DELETE FROM contacts WHERE contact_id = %s"
            cur.execute(sql_id, (contact_id,))
            deleted_rows = cur.rowcount
        except ValueError:
            # Not an ID, try by phone first (unique)
            sql_phone = "DELETE FROM contacts WHERE phone = %s"
            cur.execute(sql_phone, (identifier,))
            deleted_rows = cur.rowcount

            # If not deleted by phone, try by name (case-insensitive)
            if deleted_rows == 0:
                print(f"No contact found with ID or phone '{identifier}'. Trying by name...")
                sql_name = "DELETE FROM contacts WHERE first_name ILIKE %s OR last_name ILIKE %s"
                cur.execute(sql_name, (identifier, identifier))
                deleted_rows = cur.rowcount

        if deleted_rows > 0:
            conn.commit()
            print(f"Successfully deleted {deleted_rows} contact(s) matching '{identifier}'.")
        else:
            print(f"No contact found matching '{identifier}'.")
            conn.rollback() # No changes made

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting contact: {error}")
        conn.rollback()
    finally:
        if cur:
            cur.close()


# --- Main Menu ---

def main_menu(conn):
    """ Display the main menu and handle user choices """
    while True:
        print("\n=========== PhoneBook Manager ===========")
        print("  --- Basic Operations ---")
        print("  1. Add Contact (Console)")
        print("  2. Add Contacts (from contacts.csv)")
        print("  3. Update Contact (by ID or Phone)")
        print("  --- Advanced Operations ---")
        print("  4. Add/Update Contact (Upsert by Phone)")
        print("  5. Bulk Insert Contacts (Console w/ Validation)")
        print("  --- Querying ---")
        print("  6. Search Contacts (by Name/Phone Pattern)")
        print("  7. List Contacts (by page)")
        print("  --- Deletion ---")
        print("  8. Delete Contact (by ID/Phone/Name)")
        print("  ---------------------------------------")
        print("  9. Exit")
        print("=======================================")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            insert_from_console(conn)
        elif choice == '2':
            insert_from_csv(conn)
        elif choice == '3':
            update_contact(conn)
        elif choice == '4':
            upsert_contact(conn)
        elif choice == '5':
            bulk_insert_validated(conn)
        elif choice == '6':
            query_contacts_by_pattern(conn)
        elif choice == '7':
            query_contacts_paginated(conn)
        elif choice == '8':
            delete_contact(conn)
        elif choice == '9':
            print("Exiting PhoneBook Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

# --- Main Execution ---

if __name__ == '__main__':
    connection = connect()
    if connection:
        try:
            main_menu(connection)
        finally:
            # Ensure connection is closed even if an error occurs in the menu
            connection.close()
            print("\nDatabase connection closed.")
    else:
        print("\nFailed to connect to the database. Exiting.")

