import shelve
import os
import json

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

data_directory = config['data_directory']
database_file = config['database_file']

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
