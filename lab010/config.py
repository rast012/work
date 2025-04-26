#!/usr/bin/python
from configparser import ConfigParser
import os

def config(filename='database.ini', section='postgresql'):
    """
    Parses database configuration from a file.

    Args:
        filename (str): The name of the configuration file. Defaults to 'database.ini'.
        section (str): The section in the config file to read. Defaults to 'postgresql'.

    Returns:
        dict: A dictionary containing database connection parameters.
              Returns None if the file or section is not found.
    """
    # Construct the full path to the filename relative to this script's directory
    script_dir = os.path.dirname(__file__) #<-- Absolute dir the script is in
    abs_file_path = os.path.join(script_dir, filename)

    # Check if the config file exists
    if not os.path.exists(abs_file_path):
        print(f"Error: Configuration file '{abs_file_path}' not found.")
        # Optionally, you could check other locations here if needed
        return None # Indicate failure

    # Create a parser
    parser = ConfigParser()
    # Read config file
    parser.read(abs_file_path)

    # Get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        print(f'Error: Section "{section}" not found in the "{abs_file_path}" file.')
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
        print(f"Ensure '{config.__defaults__[0]}' exists in the same directory as config.py and has a [{config.__defaults__[1]}] section.")
