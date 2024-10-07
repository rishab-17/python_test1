budget.py

# budget.py
import os
import shelve
from constants import Category
from datetime import datetime
import csv

# Ensure the data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

class Budget:
    def __init__(self, category: Category, amount: float, start_date: str, end_date: str):
        self.category = category
        self.amount = amount
        self.start_date = start_date
        self.end_date = end_date
    
    def __str__(self):
        return f"Category: {self.category.name}, Amount: {self.amount}, Start Date: {self.start_date}, End Date: {self.end_date}"

class BudgetHandler:
    def __init__(self, db_file="data/budget_db"):
        self.db_file = db_file
    
    def addBudget(self, budget: Budget):
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
            budgets.append(budget)
            db['budgets'] = budgets  # Save back to shelve
            
            print(f"Added Budget: {budget}")  # Debugging statement
            print(f"Total Budgets in DB: {len(budgets)}")  # Check the total number of budgets after adding
            
        self.saveToCsv(budget)
    
    def saveToCsv(self, budget: Budget):
        with open('data/budgets.csv', 'a', newline="") as file:
            writer = csv.writer(file)
            writer.writerow([budget.category.name, budget.amount, budget.start_date, budget.end_date])

    def viewBudgets(self, filter_by=None, filter_value=None):
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
            print(f"Budgets retrieved from DB: {len(budgets)}")  # Debugging statement
            
        filtered_budgets = []
        for budget in budgets:
            if filter_by == "category" and budget.category.name == filter_value:
                filtered_budgets.append(budget)
            elif filter_by is None:
                filtered_budgets.append(budget)

        if filtered_budgets:
            self.displayBudgets(filtered_budgets)
        else:
            print("No budgets found for the given filter.")
    
    def displayBudgets(self, budgets):
        print("\nBudgets:")
        for budget in budgets:
            print(f"Category: {budget.category.name}, Amount: {budget.amount}, Start Date: {budget.start_date}, End Date: {budget.end_date}")


    def checkBudgetExceeded(self, expense_handler, category: Category):
        # Calculate total expenses for the selected category
        total_expenses = sum(expense.amount for expense in expense_handler.getExpensesByCategory(category.name))
        
        # Get the budget for this category
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
        
        for budget in budgets:
            if budget.category == category:
                if total_expenses > budget.amount:
                    print(f"Warning: You have exceeded your budget for {category.name}!")
                else:
                    print(f"You are within your budget for {category.name}.")
                break
        else:
            print(f"No budget found for {category.name}.")


budgetmenu.py

# budgetMenus.py
from simple_term_menu import TerminalMenu
from budget import Budget, BudgetHandler
from constants import Category
from datetime import datetime

def addBudgetMenu(handler: BudgetHandler):
    print("----- Add Budget -----")
    
    # Select Category
    category_menu = TerminalMenu([category.name for category in Category], title="Select Category:")
    category_index = category_menu.show()
    category = list(Category)[category_index]
    
    # Input Amount
    amount = float(input("Enter the budget amount: "))
    
    # Input Start Date
    while True:
        start_date_input = input("Enter the start date (YYYY-MM-DD): ")
        try:
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Try again.")
    
    # Input End Date
    while True:
        end_date_input = input("Enter the end date (YYYY-MM-DD): ")
        try:
            end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
            if end_date >= start_date:
                break
            else:
                print("End date must be after or the same as the start date.")
        except ValueError:
            print("Invalid date format. Try again.")
    
    # Create and save budget
    budget = Budget(category=category, amount=amount, start_date=start_date_input, end_date=end_date_input)
    handler.addBudget(budget)
    print("Budget added successfully!\n")


def viewBudgetMenu(handler: BudgetHandler):
    print("----- View Budgets -----")
    
    options = ["View by Category", "View All", "Back to Main Menu"]
    view_menu = TerminalMenu(options, title="Select view option:")
    choice_index = view_menu.show()

    if choice_index == 0:
        category_menu = TerminalMenu([category.name for category in Category], title="Select Category:")
        category_index = category_menu.show()
        category_name = list(Category)[category_index].name
        handler.viewBudgets(filter_by="category", filter_value=category_name)
    elif choice_index == 1:
        handler.viewBudgets()

def checkBudgetExceededMenu(handler: BudgetHandler, expense_handler):
    print("----- Check Budget -----")
    
    category_menu = TerminalMenu([category.name for category in Category], title="Select Category to Check:")
    category_index = category_menu.show()
    category = list(Category)[category_index]
    
    handler.checkBudgetExceeded(expense_handler, category)


main.py
# main.py
from simple_term_menu import TerminalMenu
from expense import ExpenseHandler
from budget import BudgetHandler
from menus import expenseMenus as expMenu, budgetMenus as budMenu

def expenseMainMenu(expense_handler: ExpenseHandler, budget_handler: BudgetHandler):
    while True:
        options = ["Add Expense", "View Expense", "View Expense Chart", 
                   "Add Budget", "View Budget", "Check Budget Exceeded", "Exit"]
        
        menu = TerminalMenu(options, title="----- Main Menu -----", menu_cursor=">", menu_cursor_style=("fg_green",))
        choice = menu.show()

        if choice == 0:
            expMenu.addExpenseMenu(expense_handler)
        elif choice == 1:
            expMenu.viewExpenseMenu(expense_handler)
        elif choice == 2:
            expMenu.viewExpenseChartMenu(expense_handler)
        elif choice == 3:
            budMenu.addBudgetMenu(budget_handler)
        elif choice == 4:
            budMenu.viewBudgetMenu(budget_handler)
        elif choice == 5:
            budMenu.checkBudgetExceededMenu(budget_handler, expense_handler)
        elif choice == 6:
            print("Exiting the program.")
            break

if __name__ == "__main__":
    expense_handler = ExpenseHandler()
    budget_handler = BudgetHandler()

    expenseMainMenu(expense_handler, budget_handler)



# simple-term-menu==1.1.0
# tabulate==0.9.0          
# matplotlib==3.7.1         
# mplcursors==0.5.2         
# shelve                   
# csv                       


import shelve
from datetime import datetime

class Budget:
    def __init__(self, category, limit_amount, frequency, period):
        self.category = category
        self.limit_amount = limit_amount
        self.frequency = frequency  # 'monthly' or 'yearly'
        self.period = period        # month/year value

    def __str__(self):
        return f"{self.category.name} budget: Rs {self.limit_amount} ({self.frequency.capitalize()} {self.period})"


class BudgetHandler:
    def __init__(self, db_file='data/budget_db'):
        self.db_file = db_file

    def add_budget(self, budget):
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
            budgets.append(budget)
            db['budgets'] = budgets
        print("Budget added successfully!")

    def view_budgets(self):
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
        if budgets:
            for budget in budgets:
                print(budget)
        else:
            print("No budgets found.")

    def check_budget_exceeded(self, expense_handler, category):
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
        # Get the budget for the category
        budget = next((b for b in budgets if b.category == category), None)

        if not budget:
            print(f"No budget set for {category.name}.")
            return False

        # Sum up expenses for that period and category
        if budget.frequency == 'monthly':
            period_filter = datetime.now().strftime("%Y-%m")
        elif budget.frequency == 'yearly':
            period_filter = datetime.now().strftime("%Y")
        
        total_expenses = sum(
            expense.amount for expense in expense_handler.getExpensesByCategory(category.name)
            if expense.date.startswith(period_filter)
        )

        if total_expenses > budget.limit_amount:
            print(f"Warning! You have exceeded the budget for {category.name}. Budget: Rs {budget.limit_amount}, Expenses: Rs {total_expenses}")
            return True
        else:
            print(f"Expenses are within the budget for {category.name}. Total spent: Rs {total_expenses}, Limit: Rs {budget.limit_amount}")
            return False

    def soft_limit_exceed(self, expense_handler, expense):
        exceeded = self.check_budget_exceeded(expense_handler, expense.category)
        if exceeded:
            choice = input("Do you still want to add this expense? (y/n): ").strip().lower()
            if choice == 'y':
                expense_handler.addExpense(expense)
                print("Expense added despite exceeding the budget.")
            else:
                print("Expense not added.")
        else:
            expense_handler.addExpense(expense)







    def add_budget_menu(budget_handler):
    while True:
        options = ["Food", "Transport", "Entertainment", "Bills", "Other", "Back to Main Menu"]
        menu = TerminalMenu(options, title="Add Budget")
        choice = menu.show()

        if choice == 5:  # Back to main menu
            break

        category = Category(choice + 1)

        # User selects the frequency (monthly/yearly)
        frequency = input("Choose budget type (monthly/yearly): ").strip().lower()
        if frequency == 'monthly':
            period = input("Enter the month (e.g. 2024-10): ")
        elif frequency == 'yearly':
            period = input("Enter the year (e.g. 2024): ")

        limit_amount = float(input("Enter the budget limit (in Rs): "))
        budget = Budget(category, limit_amount, frequency, period)

        budget_handler.add_budget(budget)


def checkBudgetExceededMenu(budget_handler, expense_handler):
    options = ["Food", "Transport", "Entertainment", "Bills", "Other"]
    menu = TerminalMenu(options, title="Check Budget Exceeded")
    choice = menu.show()

    category = Category(choice + 1)
    budget_handler.check_budget_exceeded(expense_handler, category)



########################################

def check_budget_exceeded(self, expense_handler: ExpenseHandler, category: Category):
    """
    Check if the budget for a given category (monthly/yearly) has been exceeded.
    
    Arguments:
    expense_handler -- The handler to retrieve expenses.
    category -- The category for which to check the budget.
    """
    
    # Retrieve the relevant budget for this category from the shelve database
    with shelve.open(self.db_file) as db:
        budgets = db.get('budgets', [])
        # Find the budget for the given category
        budget = next((b for b in budgets if b.category == category), None)

    if not budget:
        print(f"No budget found for {category.name}.")
        return False

    # Determine if the budget is monthly or yearly
    if budget.frequency == 'monthly':
        period = datetime.now().strftime("%Y-%m")  # Example: '2024-09' for September 2024
    elif budget.frequency == 'yearly':
        period = datetime.now().strftime("%Y")  # Example: '2024' for the entire year

    # Retrieve expenses for the given category
    expenses = expense_handler.getExpensesByCategory(category.name)

    if not expenses:
        print(f"No expenses found for {category.name} in {period}.")
        return False

    # Sum the total expenses for the relevant period (monthly or yearly)
    total_expenses = sum(
        expense.amount for expense in expenses if expense.date.startswith(period)
    )

    # Compare the total expenses with the budget amount
    if total_expenses > budget.limit_amount:
        print(f"Budget for {category.name} in {period} is Rs {budget.limit_amount}. Expenses in {period} are Rs {total_expenses}. Budget exceeded!")
        return True
    else:
        print(f"Budget for {category.name} in {period} is Rs {budget.limit_amount}. Expenses in {period} are Rs {total_expenses}. Budget not exceeded.")
        return False


############################################################

def check_budget_exceeded(self, expense_handler: ExpenseHandler, category: Category):
    """
    Check if the budget for a given category has been exceeded based on the budget's period (monthly/yearly).
    
    Arguments:
    expense_handler -- The handler to retrieve expenses.
    category -- The category for which to check the budget.
    """
    
    # Retrieve the relevant budget for this category from the shelve database
    with shelve.open(self.db_file) as db:
        budgets = db.get('budgets', [])
        # Find the budget for the given category
        budget = next((b for b in budgets if b.category == category), None)

    if not budget:
        print(f"No budget found for {category.name}.")
        return False

    # Determine the period based on the budget frequency
    if budget.frequency == 'monthly':
        period_filter = budget.period  # e.g., '2024-09' for September 2024
    elif budget.frequency == 'yearly':
        period_filter = budget.period  # e.g., '2024' for the entire year

    # Retrieve expenses for the given category
    expenses = expense_handler.getExpensesByCategory(category.name)

    if not expenses:
        print(f"No expenses found for {category.name} in {period_filter}.")
        return False

    # Filter expenses by the budget period
    total_expenses = sum(
        expense.amount for expense in expenses if expense.date.startswith(period_filter)
    )

    # Compare total expenses with the budget amount
    if total_expenses > budget.limit_amount:
        print(f"Budget for {category.name} in {period_filter} is Rs {budget.limit_amount}. Expenses in {period_filter} are Rs {total_expenses}. Budget exceeded!")
        return True
    else:
        print(f"Budget for {category.name} in {period_filter} is Rs {budget.limit_amount}. Expenses in {period_filter} are Rs {total_expenses}. Budget not exceeded.")
        return False


###################################################################################
def check_budget_exceeded(self, expense_handler: ExpenseHandler, category: Category):
    """
    Check if the budget for a given category has been exceeded for each budget period (monthly/yearly).
    
    Arguments:
    expense_handler -- The handler to retrieve expenses.
    category -- The category for which to check all relevant budgets.
    """

    # Retrieve all budgets for the given category from the shelve database
    with shelve.open(self.db_file) as db:
        budgets = db.get('budgets', [])
        # Filter budgets to only those relevant to the passed category
        category_budgets = [b for b in budgets if b.category == category]

    if not category_budgets:
        print(f"No budgets found for {category.name}.")
        return False

    # Retrieve expenses for the given category
    expenses = expense_handler.getExpensesByCategory(category.name)

    if not expenses:
        print(f"No expenses found for {category.name}.")
        return False

    # Now, for each budget in the category, check the budget period and compare against expenses
    for budget in category_budgets:
        # Determine the period (monthly or yearly) based on the budget frequency
        if budget.frequency == 'monthly':
            period_filter = budget.period  # e.g., '2024-09' for September 2024
        elif budget.frequency == 'yearly':
            period_filter = budget.period  # e.g., '2024' for the entire year

        # Calculate total expenses for the specific period
        total_expenses = sum(
            expense.amount for expense in expenses if expense.date.startswith(period_filter)
        )

        # Compare total expenses with the budget amount for this period
        if total_expenses > budget.limit_amount:
            print(f"Budget for {category.name} in {period_filter} is Rs {budget.limit_amount}. Expenses in {period_filter} are Rs {total_expenses}. Budget exceeded!")
        else:
            print(f"Budget for {category.name} in {period_filter} is Rs {budget.limit_amount}. Expenses in {period_filter} are Rs {total_expenses}. Budget not exceeded.")
    
    return True

####################################################

import unittest
import os
import shelve
from constants import Category
from budget import Budget, BudgetHandler

class TestBudget(unittest.TestCase):

    def setUp(self):
        """Set up a fresh shelve database for each test."""
        self.db_file = './data/test_budget_db'
        self.budget_handler = BudgetHandler(db_file=self.db_file)

        # Ensure test files are reset
        if os.path.exists(self.db_file):
            os.remove(self.db_file + '.db')

    def tearDown(self):
        """Clean up test database after each test."""
        if os.path.exists(self.db_file):
            os.remove(self.db_file + '.db')

    def test_add_budget(self):
        """Test adding a new budget."""
        budget = Budget(category=Category.FOOD, limit=5000, period="monthly", period_value="2024-10")
        self.budget_handler.add_budget(budget)

        # Verify that budget was saved in shelve
        with shelve.open(self.db_file) as db:
            budgets = db.get('budgets', [])
            self.assertEqual(len(budgets), 1)
            self.assertEqual(budgets[0].category, Category.FOOD)
            self.assertEqual(budgets[0].limit, 5000)

    def test_budget_exceeded(self):
        """Test checking if a budget is exceeded."""
        budget = Budget(category=Category.TRANSPORT, limit=2000, period="monthly", period_value="2024-10")
        self.budget_handler.add_budget(budget)

        # Add some expenses and verify budget check
        expense_1 = Expense(category=Category.TRANSPORT, amount=1500, date="2024-10-06", description="Bus fare")
        expense_2 = Expense(category=Category.TRANSPORT, amount=600, date="2024-10-07", description="Taxi fare")
        self.budget_handler.add_expense(expense_1)
        self.budget_handler.add_expense(expense_2)

        # Check if budget exceeded
        exceeded = self.budget_handler.check_budget_exceeded(Category.TRANSPORT)
        self.assertTrue(exceeded)

    def test_budget_not_exceeded(self):
        """Test checking if a budget is not exceeded."""
        budget = Budget(category=Category.FOOD, limit=3000, period="monthly", period_value="2024-10")
        self.budget_handler.add_budget(budget)

        # Add some expenses and verify budget check
        expense_1 = Expense(category=Category.FOOD, amount=500, date="2024-10-06", description="Lunch")
        expense_2 = Expense(category=Category.FOOD, amount=1000, date="2024-10-07", description="Dinner")
        self.budget_handler.add_expense(expense_1)
        self.budget_handler.add_expense(expense_2)

        # Check if budget exceeded
        exceeded = self.budget_handler.check_budget_exceeded(Category.FOOD)
        self.assertFalse(exceeded)

    def test_view_budgets(self):
        """Test viewing all budgets."""
        budget_1 = Budget(category=Category.ENTERTAINMENT, limit=1000, period="yearly", period_value="2024")
        budget_2 = Budget(category=Category.FOOD, limit=3000, period="monthly", period_value="2024-10")
        self.budget_handler.add_budget(budget_1)
        self.budget_handler.add_budget(budget_2)

        # Fetch all budgets and verify
        budgets = self.budget_handler.view_budgets()
        self.assertEqual(len(budgets), 2)
        self.assertEqual(budgets[0].category, Category.ENTERTAINMENT)
        self.assertEqual(budgets[1].category, Category.FOOD)

if __name__ == '__main__':
    unittest.main()
