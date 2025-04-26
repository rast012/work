from configparser import ConfigParser
import os

def config(filename='database.ini', section='postgresql'):
    """
    Parses database configuration from a file.

    Args:
        filename (str): The name of the configuration file.
        section (str): The section in the config file to read (e.g., 'postgresql').

    Returns:
        dict: A dictionary containing database connection parameters.
              Returns None if the file or section is not found.
    """
    # Check if the config file exists in the current directory
    if not os.path.exists(filename):
        print(f"Error: Configuration file '{filename}' not found.")
        # Try checking in a parent directory if running from a subdirectory (optional)
        parent_dir_filename = os.path.join(os.path.dirname(__file__), '..', filename)
        if os.path.exists(parent_dir_filename):
             filename = parent_dir_filename
        else:
            print(f"Error: Also not found in parent directory.")
            return None # Indicate failure

    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(filename)

    # Get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        print(f'Error: Section {section} not found in the {filename} file.')
        return None # Indicate failure

    return db

# Example usage (optional, for testing this file directly)
if __name__ == '__main__':
    db_params = config()
    if db_params:
        print("Database config loaded successfully:")
        print(db_params)
    else:
        print("Failed to load database config.")
        print("Ensure 'database.ini' exists and has a [postgresql] section.")

