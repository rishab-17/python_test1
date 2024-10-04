import argparse
import json
import os
import sys
from simple_term_menu import TerminalMenu
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


def pause():
    """Pause the terminal so the user can see the output."""
    input("\nPress Enter to continue...")


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
    pause()


def view_expenses():
    """View all expenses"""
    expenses = load_expenses()
    if expenses:
        for exp in expenses:
            print(f"{exp.date}: {exp.category} - {exp.amount}")
    else:
        print("No expenses recorded.")
    pause()


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
    pause()


def generate_report():
    """Generate and display an expense report"""
    print("Generating monthly expense report...")

    # Load expenses from the database
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded.")
        pause()
        return

    # Generate a monthly report (or adjust for other periods as needed)
    report_data = generate_monthly_report(expenses)

    # Display the report in ASCII bar chart form
    print("\nExpense Report (by category):")
    plot_ascii_bar_chart(report_data)
    pause()


def cli_menu():
    """Display the interactive menu using simple-term-menu"""
    options = [
        "1. Add an Expense",
        "2. View Expenses",
        "3. Set a Budget",
        "4. Generate Expense Report",
        "5. Exit"
    ]
    menu = TerminalMenu(options)

    while True:
        menu_entry_index = menu.show()
        if menu_entry_index == 0:
            add_expense()
        elif menu_entry_index == 1:
            view_expenses()
        elif menu_entry_index == 2:
            set_budget()
        elif menu_entry_index == 3:
            generate_report()
        elif menu_entry_index == 4:
            print("Exiting...")
            break


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Personal Finance Manager CLI")

    # Add an argument to decide whether to use the menu or direct commands
    parser.add_argument(
        "--menu",
        action="store_true",
        help="Launch the interactive menu-based interface"
    )

    # Parse the arguments
    args = parser.parse_args()

    # If --menu is specified, use the interactive menu
    if args.menu:
        cli_menu()
    else:
        # If no menu is specified, use standard argparse commands (for CLI users)
        print("Welcome to the Personal Finance Manager!")
        print("Use --menu for the interactive menu or implement other argparse commands.")

if __name__ == "__main__":
    main()


# import argparse
# import json
# import os
# import sys
# from simple_term_menu import TerminalMenu
# from colorama import Fore, Style, init
# from expense import Expense, save_expense, load_expenses
# from budget import Budget
# from report import generate_monthly_report, plot_ascii_bar_chart

# # Initialize Colorama
# init(autoreset=True)

# # Load configuration from config.json
# config_path = os.path.join(os.path.dirname(__file__), 'config.json')
# try:
#     with open(config_path) as config_file:
#         config = json.load(config_file)
#         data_directory = config['data_directory']
#         database_file = config['database_file']
# except FileNotFoundError:
#     print(f"Error: {config_path} not found.")
#     data_directory = 'data/'  # Fallback default
#     database_file = 'datastore.db'
# except json.JSONDecodeError as e:
#     print(f"Error: Invalid JSON format in {config_path}: {e}")
#     data_directory = 'data/'
#     database_file = 'datastore.db'


# def pause():
#     """Pause the terminal so the user can see the output."""
#     input("\nPress Enter to continue...")


# def add_expense():
#     """Add a new expense"""
#     amount = float(input('Enter amount: '))
#     category = input('Enter category (e.g., Food, Transport): ')
#     date = input('Enter date (YYYY-MM-DD): ')

#     # Create an Expense object
#     exp = Expense(amount, category, date)

#     # Save the expense
#     save_expense(exp)
#     print(f"Expense of {amount} added to category '{category}' on {date}")
#     pause()


# def view_expenses():
#     """View all expenses"""
#     expenses = load_expenses()
#     if expenses:
#         for exp in expenses:
#             print(f"{exp.date}: {exp.category} - {exp.amount}")
#     else:
#         print("No expenses recorded.")
#     pause()


# def set_budget():
#     """Set a budget for a category and period"""
#     category = input('Enter category: ')
#     limit = float(input('Enter limit: '))
#     period = input('Enter period (monthly/yearly): ')

#     # Create a Budget object
#     budget = Budget(category, limit, period)

#     # Load expenses and check if budget is exceeded
#     expenses = load_expenses()
#     if budget.is_over_budget(expenses):
#         print(f"Warning: You have exceeded your {period} budget for {category}!")
#     else:
#         print(f"Your {period} budget for {category} is within limits.")
#     pause()


# def generate_report():
#     """Generate and display an expense report"""
#     print("Generating monthly expense report...")

#     # Load expenses from the database
#     expenses = load_expenses()
#     if not expenses:
#         print("No expenses recorded.")
#         pause()
#         return

#     # Generate a monthly report (or adjust for other periods as needed)
#     report_data = generate_monthly_report(expenses)

#     # Display the report in ASCII bar chart form
#     print("\nExpense Report (by category):")
#     plot_ascii_bar_chart(report_data)
#     pause()


# def cli_menu():
#     """Display the interactive menu using simple-term-menu"""
#     options = [
#         f"{Fore.GREEN}Add an Expense{Style.RESET_ALL}",
#         f"{Fore.GREEN}View Expenses{Style.RESET_ALL}",
#         f"{Fore.GREEN}Set a Budget{Style.RESET_ALL}",
#         f"{Fore.GREEN}Generate Expense Report{Style.RESET_ALL}",
#         f"{Fore.RED}Exit{Style.RESET_ALL}"
#     ]

#     # Create the terminal menu
#     menu = TerminalMenu(options, title="===== Personal Finance Manager =====", 
#                         subtitle="Choose an option:",
#                         menu_cursor=Fore.CYAN + "→" + Style.RESET_ALL)

#     while True:
#         menu_entry_index = menu.show()
#         if menu_entry_index == 0:
#             add_expense()
#         elif menu_entry_index == 1:
#             view_expenses()
#         elif menu_entry_index == 2:
#             set_budget()
#         elif menu_entry_index == 3:
#             generate_report()
#         elif menu_entry_index == 4:
#             print("Exiting...")
#             break


# def main():
#     # Create argument parser
#     parser = argparse.ArgumentParser(description="Personal Finance Manager CLI")

#     # Add an argument to decide whether to use the menu or direct commands
#     parser.add_argument(
#         "--menu",
#         action="store_true",
#         help="Launch the interactive menu-based interface"
#     )

#     # Parse the arguments
#     args = parser.parse_args()

#     # If --menu is specified, use the interactive menu
#     if args.menu:
#         cli_menu()
#     else:
#         # If no menu is specified, use standard argparse commands (for CLI users)
#         print("Welcome to the Personal Finance Manager!")
#         print("Use --menu for the interactive menu or implement other argparse commands.")

# if __name__ == "__main__":
#     main()
