import psycopg2
import csv
import sys
from config import config # Import the config function from config.py

# --- New Functions for pattern search, upsert, bulk insert, pagination, delete ---

def get_by_pattern(conn, pattern):
    """
    Returns all contacts where first_name, last_name or phone matches the pattern (case-insensitive).
    """
    sql = """
        SELECT contact_id, first_name, last_name, phone, created_at
          FROM phonebook
         WHERE first_name ILIKE %(pat)s
            OR last_name  ILIKE %(pat)s
            OR phone      ILIKE %(pat)s
         ORDER BY first_name, last_name
    """
    with conn.cursor() as cur:
        cur.execute(sql, {'pat': f"%{pattern}%"})
        rows = cur.fetchall()
    return rows


def upsert_user(conn, first_name, last_name, phone):
    """
    Inserts a new user or updates the phone if user already exists by name.
    Returns True if inserted or updated, False on error.
    """
    try:
        with conn.cursor() as cur:
            # Check existence
            cur.execute(
                "SELECT contact_id FROM phonebook WHERE first_name = %s AND \
                 COALESCE(last_name, '') = COALESCE(%s, '')",
                (first_name, last_name)
            )
            found = cur.fetchone()
            if found:
                cur.execute(
                    "UPDATE phonebook SET phone = %s WHERE contact_id = %s",
                    (phone, found[0])
                )
            else:
                cur.execute(
                    "INSERT INTO phonebook(first_name, last_name, phone) VALUES(%s, %s, %s)",
                    (first_name, last_name, phone)
                )
        conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error in upsert_user: {error}")
        conn.rollback()
        return False


def insert_many_users(conn, entries):
    """
    entries: list of tuples (first_name, last_name, phone)
    Validates phone (digits only). Returns list of invalid entries.
    Inserts or updates valid ones via upsert_user.
    """
    invalid = []
    for first_name, last_name, phone in entries:
        if not phone or not re.fullmatch(r'\d+', phone):
            invalid.append((first_name, last_name, phone))
            continue
        success = upsert_user(conn, first_name, last_name, phone)
        if not success:
            invalid.append((first_name, last_name, phone))
    return invalid


def query_with_pagination(conn, limit, offset):
    """
    Returns contacts with pagination.
    """
    sql = """
        SELECT contact_id, first_name, last_name, phone, created_at
          FROM phonebook
         ORDER BY contact_id
         LIMIT %s OFFSET %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (limit, offset))
        return cur.fetchall()


def delete_user(conn, first_name=None, last_name=None, phone=None):
    """
    Deletes contacts matching first/last name or phone.
    Returns number of deleted rows.
    """
    clauses = []
    params = []

    if phone:
        clauses.append("phone = %s")
        params.append(phone)
    if first_name:
        clauses.append("first_name = %s")
        params.append(first_name)
    if last_name is not None:
        clauses.append("last_name = %s")
        params.append(last_name)

    if not clauses:
        print("Error: must provide at least first_name, last_name, or phone to delete.")
        return 0

    sql = f"DELETE FROM phonebook WHERE {' OR '.join(clauses)}"
    with conn.cursor() as cur:
        cur.execute(sql, params)
        deleted = cur.rowcount
    conn.commit()
    return deleted

# --- Existing functions ---

def connect():
    conn = None
    try:
        params = config()
        if params is None:
            print("Database configuration could not be loaded. Exiting.")
            sys.exit(1)
        conn = psycopg2.connect(**params)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting: {error}")
        sys.exit(1)
    return conn

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Read connection parameters
        params = config()
        if params is None:
             print("Database configuration could not be loaded. Exiting.")
             sys.exit(1) # Exit if config fails

        # Connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connection successful.')

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error connecting to database: {error}")
        sys.exit(1) # Exit if connection fails

    return conn

def create_table(conn):
    #Create the phonebook table 
    command = """
        CREATE TABLE IF NOT EXISTS phonebook (
            contact_id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100),
            phone VARCHAR(20) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        with conn.cursor() as cur:
            cur.execute(command)
        conn.commit()
        print("Table 'phonebook' checked/created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
        conn.rollback() # Roll back changes on error

def insert_from_console(conn):
    # Insert a new contact into the phonebook table from console input 
    try:
        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name (optional, press Enter to skip): ").strip()
        phone = input("Enter phone number: ").strip()

        if not first_name or not phone:
            print("First name and phone number cannot be empty.")
            return

        sql = """INSERT INTO phonebook(first_name, last_name, phone)
                 VALUES(%s, %s, %s) RETURNING contact_id;"""
        contact_id = None

        with conn.cursor() as cur:
            # Use None for last_name if it's empty
            cur.execute(sql, (first_name, last_name if last_name else None, phone))
            # Get the generated id back
            contact_id = cur.fetchone()[0]
            # Commit the changes to the database
            conn.commit()
        print(f"Contact '{first_name} {last_name}' with phone '{phone}' added successfully with ID: {contact_id}.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting contact: {error}")
        conn.rollback()

def insert_from_csv(conn, csv_filepath):
    """ Insert multiple contacts into the phonebook table from a CSV file """
    sql = "INSERT INTO phonebook(first_name, last_name, phone) VALUES(%s, %s, %s)"
    inserted_count = 0
    skipped_count = 0

    try:
        with open(csv_filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader, None) # Skip header row if it exists

            if not header or len(header) < 2: # Expecting at least first_name, phone
                 print("CSV file must have at least 'first_name' and 'phone' columns.")
                 return

            print(f"Processing CSV file: {csv_filepath}")
            with conn.cursor() as cur:
                for row in reader:
                    try:
                        if len(row) >= 2:
                            first_name = row[0].strip()
                            # Handle optional last name (assuming it's the second column if present)
                            last_name = row[1].strip() if len(row) > 1 and row[1].strip() else None
                            # Handle phone number (assuming it's the last column provided, or 2nd if no last name)
                            phone_col_index = 2 if last_name else 1
                            if len(row) > phone_col_index:
                                phone = row[phone_col_index].strip()
                                if first_name and phone: # Basic validation
                                     cur.execute(sql, (first_name, last_name, phone))
                                     inserted_count += 1
                                else:
                                     print(f"Skipping row due to missing first name or phone: {row}")
                                     skipped_count += 1
                            else:
                                print(f"Skipping row due to missing phone number: {row}")
                                skipped_count += 1
                        else:
                             print(f"Skipping row due to insufficient columns: {row}")
                             skipped_count += 1
                    except (Exception, psycopg2.DatabaseError) as row_error:
                        print(f"Error inserting row {row}: {row_error}. Skipping row.")
                        conn.rollback() # Rollback the single failed insert attempt
                        skipped_count += 1
                        # It's often better to continue processing other rows
                        # Re-establish connection state if necessary after rollback within loop
                        # For simplicity here, we just print and skip.
                        # A robust solution might collect failed rows.


                conn.commit() # Commit all successful inserts
        print(f"CSV import complete. Inserted: {inserted_count}, Skipped: {skipped_count}.")

    except FileNotFoundError:
        print(f"Error: CSV file not found at '{csv_filepath}'")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error during CSV import: {error}")
        conn.rollback()

def update_contact(conn):
    """ Update contact's first name or phone number based on phone number """
    try:
        phone_to_update = input("Enter the CURRENT phone number of the contact to update: ").strip()
        if not phone_to_update:
            print("Phone number cannot be empty.")
            return

        # Check if contact exists
        existing_contact = query_data(conn, phone_filter=phone_to_update, display=False)
        if not existing_contact:
            print(f"No contact found with phone number '{phone_to_update}'.")
            return

        print(f"Found contact: {existing_contact[0]}") # Display current details

        new_first_name = input("Enter new first name (or press Enter to keep current): ").strip()
        new_phone = input("Enter new phone number (or press Enter to keep current): ").strip()

        if not new_first_name and not new_phone:
            print("No changes specified.")
            return

        updates = []
        params = []

        if new_first_name:
            updates.append("first_name = %s")
            params.append(new_first_name)
        if new_phone:
            updates.append("phone = %s")
            params.append(new_phone)

        params.append(phone_to_update) # For the WHERE clause

        sql = f"UPDATE phonebook SET {', '.join(updates)} WHERE phone = %s"

        updated_rows = 0
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            updated_rows = cur.rowcount
            conn.commit()

        if updated_rows > 0:
            print(f"Contact with original phone '{phone_to_update}' updated successfully.")
        else:
            # Should not happen if check passed, but good to handle
            print(f"Failed to update contact with phone '{phone_to_update}'. It might have been deleted.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error updating contact: {error}")
        conn.rollback()

def query_data(conn, first_name_filter=None, last_name_filter=None, phone_filter=None, display=True):
    """ Query contacts with optional filters """
    base_sql = "SELECT contact_id, first_name, last_name, phone, created_at FROM phonebook"
    filters = []
    params = []

    if first_name_filter:
        filters.append("first_name ILIKE %s") # Case-insensitive search
        params.append(f"%{first_name_filter}%")
    if last_name_filter:
        filters.append("last_name ILIKE %s")
        params.append(f"%{last_name_filter}%")
    if phone_filter:
        # Use exact match or LIKE depending on needs, exact match used here
        filters.append("phone = %s")
        params.append(phone_filter)

    if filters:
        sql = f"{base_sql} WHERE {' AND '.join(filters)} ORDER BY first_name, last_name"
    else:
        sql = f"{base_sql} ORDER BY first_name, last_name"

    results = []
    try:
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            if display:
                print(f"\n--- Query Results ({cur.rowcount} found) ---")
            rows = cur.fetchall()
            if rows:
                for row in rows:
                     results.append(row)
                     if display:
                         # Format output nicely
                         contact_id, fname, lname, ph, created = row
                         lname_display = lname if lname else "" # Handle None last name
                         print(f"ID: {contact_id}, Name: {fname} {lname_display}, Phone: {ph}, Added: {created.strftime('%Y-%m-%d %H:%M')}")
            elif display:
                print("No contacts found matching the criteria.")
            if display:
                 print("------------------------------")


    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error querying data: {error}")

    return results # Return results for potential internal use (like in update)


def delete_contact(conn):
    """ Delete a contact by phone number """
    try:
        phone_to_delete = input("Enter the phone number of the contact to delete: ").strip()
        if not phone_to_delete:
            print("Phone number cannot be empty.")
            return

        # Optional: Confirm before deleting
        confirm = input(f"Are you sure you want to delete the contact with phone '{phone_to_delete}'? (yes/no): ").lower()
        if confirm != 'yes':
            print("Deletion cancelled.")
            return

        sql = "DELETE FROM phonebook WHERE phone = %s"
        deleted_rows = 0

        with conn.cursor() as cur:
            cur.execute(sql, (phone_to_delete,))
            deleted_rows = cur.rowcount
            conn.commit()

        if deleted_rows > 0:
            print(f"Contact with phone '{phone_to_delete}' deleted successfully.")
        else:
            print(f"No contact found with phone number '{phone_to_delete}'.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error deleting contact: {error}")
        conn.rollback()

def display_menu():
    """ Displays the main menu options """
    print("\n--- Phonebook Menu ---")
    print("1. Add Contact (Console)")
    print("2. Add Contacts (CSV)")
    print("3. Update Contact")
    print("4. Query Contacts")
    print("5. Delete Contact")
    print("6. Exit")
    print("----------------------")

def run_phonebook():
    """ Main function to run the phonebook application """
    conn = connect()
    if conn is None:
        return # Exit if connection failed

    try:
        # Ensure table exists
        create_table(conn)

        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                insert_from_console(conn)
            elif choice == '2':
                csv_path = input("Enter the path to the CSV file: ").strip()
                # Basic check if path seems valid (optional)
                if not csv_path.lower().endswith('.csv'):
                     print("Please provide a valid path to a .csv file.")
                     continue
                insert_from_csv(conn, csv_path)
            elif choice == '3':
                update_contact(conn)
            elif choice == '4':
                print("\n--- Query Filters (leave blank to ignore) ---")
                fname_filter = input("Filter by First Name: ").strip()
                lname_filter = input("Filter by Last Name: ").strip()
                phone_filter = input("Filter by Phone Number: ").strip()
                query_data(conn,
                           first_name_filter=fname_filter if fname_filter else None,
                           last_name_filter=lname_filter if lname_filter else None,
                           phone_filter=phone_filter if phone_filter else None)
            elif choice == '5':
                delete_contact(conn)
            elif choice == '6':
                print("Exiting Phonebook.")
                break
            else:
                print("Invalid choice. Please try again.")

    except (Exception, KeyboardInterrupt) as e:
         print(f"\nAn error occurred or operation cancelled: {e}")
    finally:
        # Close the communication with the PostgreSQL database server
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    run_phonebook()
