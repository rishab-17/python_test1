import shelve
import os

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

class Expense:
    def __init__(self, amount, category, date):
        self.amount = amount
        self.category = category
        self.date = date

    def __str__(self):
        return f"{self.date}: {self.category} - {self.amount}"

# Function to save an expense to the shelve database
def save_expense(expense):
    with shelve.open('data/datastore.db', writeback=True) as db:
        if 'expenses' not in db:
            db['expenses'] = []  # Initialize an empty list if it doesn't exist
        db['expenses'].append(expense)
        db.sync()  # Ensure data is written to disk

# Function to load all expenses from the shelve database
def load_expenses():
    with shelve.open('data/datastore.db') as db:
        return db.get('expenses', [])
