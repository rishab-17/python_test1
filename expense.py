import shelve
import os
import json

# Path to config.json
config_path = os.path.join(os.path.dirname(__file__), 'config.json')

# Load the config file
try:
    with open(config_path) as config_file:
        config = json.load(config_file)
        data_directory = config['data_directory']
        database_file = config['database_file']
except FileNotFoundError:
    print(f"Error: {config_path} not found.")
    data_directory = 'data/'
    database_file = 'datastore.db'
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in {config_path}: {e}")

# Use the loaded values
print(f"Data Directory: {data_directory}, Database File: {database_file}")


# Ensure the data directory exists
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

class Expense:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self):
        return f"{self.date}: {self.category} - {self.amount}"

# Function to save an expense to the shelve database
def save_expense(expense):
    db_path = os.path.join(data_directory, database_file)
    with shelve.open(db_path, writeback=True) as db:
        if 'expenses' not in db:
            db['expenses'] = []  # Initialize an empty list if it doesn't exist
        db['expenses'].append(expense)
        db.sync()  # Ensure data is written to disk

# Function to load all expenses from the shelve database
def load_expenses():
    db_path = os.path.join(data_directory, database_file)
    with shelve.open(db_path) as db:
        return db.get('expenses', [])
