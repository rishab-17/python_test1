import argparse
from expense import Expense, save_expense, load_expenses
from income import Income
from budget import Budget
from report import generate_monthly_report, plot_ascii_bar_chart

def main():
    # Create an argument parser for command-line arguments
    parser = argparse.ArgumentParser(description='Personal Finance Manager')
    
    # Define the commands that the user can use
    parser.add_argument('command', choices=['add_expense', 'view_expenses', 'set_budget'])
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    if args.command == 'add_expense':
        # Add a new expense
        amount = float(input('Enter amount: '))
        category = input('Enter category (e.g., Food, Transport): ')
        date = input('Enter date (YYYY-MM-DD): ')
        
        # Create an Expense object
        exp = Expense(amount, category, date)
        
        # Save the expense
        save_expense(exp)
        print(f"Expense of {amount} added to category '{category}' on {date}")
    
    elif args.command == 'view_expenses':
        # View all expenses
        expenses = load_expenses()
        if expenses:
            for exp in expenses:
                print(f"{exp.date}: {exp.category} - {exp.amount}")
        else:
            print("No expenses recorded.")
    
    elif args.command == 'set_budget':
        # Set a budget for a category
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
    
if __name__ == "__main__":
    main()
