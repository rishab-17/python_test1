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
