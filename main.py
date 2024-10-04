# import argparse
# from expense import Expense, save_expense, load_expenses
# from budget import Budget
# from report import generate_monthly_report, plot_ascii_bar_chart

# def main():
#     # Create an argument parser for command-line arguments
#     parser = argparse.ArgumentParser(description='Personal Finance Manager')
    
#     # Define the commands that the user can use
#     parser.add_argument('command', choices=['add_expense', 'view_expenses', 'set_budget', 'view_report'])
    
#     # Parse the command-line arguments
#     args = parser.parse_args()
    
#     if args.command == 'add_expense':
#         # Add a new expense
#         amount = float(input('Enter amount: '))
#         category = input('Enter category (e.g., Food, Transport): ')
#         date = input('Enter date (YYYY-MM-DD): ')
        
#         # Create an Expense object
#         exp = Expense(amount, category, date)
        
#         # Save the expense
#         save_expense(exp)
#         print(f"Expense of {amount} added to category '{category}' on {date}")
    
#     elif args.command == 'view_expenses':
#         # View all expenses
#         expenses = load_expenses()
#         if expenses:
#             for exp in expenses:
#                 print(f"{exp.date}: {exp.category} - {exp.amount}")
#         else:
#             print("No expenses recorded.")
    
#     elif args.command == 'set_budget':
#         # Set a budget for a category
#         category = input('Enter category: ')
#         limit = float(input('Enter limit: '))
#         period = input('Enter period (monthly/yearly): ')
        
#         # Create a Budget object
#         budget = Budget(category, limit, period)
        
#         # Load expenses and check if budget is exceeded
#         expenses = load_expenses()
#         if budget.is_over_budget(expenses):
#             print(f"Warning: You have exceeded your {period} budget for {category}!")
#         else:
#             print(f"Your {period} budget for {category} is within limits.")

#     elif args.command == 'view_report':
#         print("Generating monthly expense report...")
        
#         # Load expenses from the database
#         expenses = load_expenses()
#         if not expenses:
#             print("No expenses recorded.")
#             return
        
#         # Generate a monthly report (or adjust for other periods as needed)
#         report_data = generate_monthly_report(expenses)
        
#         # Display the report in ASCII bar chart form
#         print("\nExpense Report (by category):")
#         plot_ascii_bar_chart(report_data)
    
# if __name__ == "__main__":
#     main()


import json
import os
from expense import Expense, save_expense, load_expenses
from budget import Budget
from report import generate_monthly_report, plot_ascii_bar_chart

# Load configuration from config.json
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
try:
    with open(config_path) as config_file:
        config = json.load(config_file)
        data_directory = config['data_directory']
        database_file = config['database_file']
except FileNotFoundError:
    print(f"Error: {config_path} not found.")
    data_directory = 'data/'  # Fallback default
    database_file = 'datastore.db'
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in {config_path}: {e}")
    data_directory = 'data/'
    database_file = 'datastore.db'

def add_expense():
    """Add a new expense"""
    amount = float(input('Enter amount: '))
    category = input('Enter category (e.g., Food, Transport): ')
    date = input('Enter date (YYYY-MM-DD): ')

    # Create an Expense object
    exp = Expense(amount, category, date)

    # Save the expense
    save_expense(exp)
    print(f"Expense of {amount} added to category '{category}' on {date}")

def view_expenses():
    """View all expenses"""
    expenses = load_expenses()
    if expenses:
        for exp in expenses:
            print(f"{exp.date}: {exp.category} - {exp.amount}")
    else:
        print("No expenses recorded.")

def set_budget():
    """Set a budget for a category and period"""
    category = input('Enter category: ')
    limit = float(input('Enter limit: '))
    period = input('Enter period (monthly/yearly): ')

    # Create a Budget object
    budget = Budget(category, limit, period)

    # Load expenses and check if budget is exceeded
    expenses = load_expenses()
    if budget.is_over_budget(expenses):
        print(f"Warning: You have exceeded your {period} budget for {category}!")
    else:
        print(f"Your {period} budget for {category} is within limits.")

def generate_report():
    """Generate and display an expense report"""
    print("Generating monthly expense report...")
    
    # Load expenses from the database
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
        return
    
    # Generate a monthly report (or adjust for other periods as needed)
    report_data = generate_monthly_report(expenses)
    
    # Display the report in ASCII bar chart form
    print("\nExpense Report (by category):")
    plot_ascii_bar_chart(report_data)

def menu():
    """Display the menu and handle user input"""
    while True:
        print("\n===== Personal Finance Manager =====")
        print("1. Add an Expense")
        print("2. View Expenses")
        print("3. Set a Budget")
        print("4. Generate Expense Report")
        print("5. Exit")
        
        choice = input("Choose an option (1-5): ")
        
        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            set_budget()
        elif choice == '4':
            generate_report()
        elif choice == '5':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    menu()
