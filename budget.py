class Budget:
    def __init__(self, category, limit, period):
        self.category = category
        self.limit = limit
        self.period = period

    def is_over_budget(self, expenses):
        total = sum(exp.amount for exp in expenses if exp.category == self.category)
        return total > self.limit


### 1. **Introduction about the Project: Financial Manager**

# The **Financial Manager** is a Python-based expense and budget management system designed to help users track their spending and manage budgets effectively. It allows users to categorize expenses, set monthly or yearly budgets, and track their financial habits in real-time. The system ensures that users can monitor their expenses per category and receive alerts when they are nearing or exceeding set budget limits.

# The core features include:
# - **Expense Tracking:** Users can add, view, and categorize expenses by date.
# - **Budget Management:** The system allows the creation of budgets for different categories (like food, transport, etc.) for monthly or yearly periods.
# - **Budget Alerts:** The system checks if a budget has been exceeded and provides users with immediate feedback.
# - **Data Storage:** All expenses and budgets are stored using `csv` files and `shelve` (a Python-based persistent storage), ensuring easy data management and retrieval.

# The system is designed with simplicity in mind, offering a terminal-based user interface for easy navigation and management of financial data.

# ---

# ### 2. **Project Design and Scope: Financial Manager**

# #### **Design Overview**

# The **Financial Manager** system follows a modular design with a focus on:
# - **Expense Management**
# - **Budget Management**
# - **Testing for Validation**
  
# Each module is responsible for its own functionality, with a clear separation between expense handling, budget operations, and testing.

# ##### **Key Modules:**

# 1. **Expense Module:**
#    - Handles creation and storage of expenses.
#    - Expenses can be categorized (food, transport, etc.) and stored with date, amount, and description.
#    - The system retrieves expenses by category and date to check if they match a budget's period (monthly/yearly).
#    - Implements methods for adding, viewing, and filtering expenses.

# 2. **Budget Module:**
#    - Users can define budgets by category, either on a monthly or yearly basis.
#    - Budgets are compared with expenses to check if the spending is within limits.
#    - Key methods include creating budgets, checking if the budget is exceeded, and soft limits (user confirmation if budget is exceeded).

# 3. **Test Module:**
#    - Unit testing using the `unittest` framework ensures that the functionality is working correctly.
#    - Tests cover adding expenses, viewing expenses by category and date, and ensuring the budgets are working correctly.

# ##### **Data Storage:**
#    - **Shelve Module:** Used for storing and retrieving expenses and budgets.
#    - **CSV Files:** Act as a backup and alternative for exporting data.

# #### **Scope of the Project:**

# The project aims to provide users with a tool to manage personal finances in an efficient, organized way. The following functionalities define the scope of the Financial Manager:

# - **Expense Tracking:** Add and retrieve expenses for specified categories and dates.
# - **Budget Monitoring:** Set monthly/yearly budgets and monitor spending in real-time. Alert the user if the budget is exceeded.
# - **Expense and Budget Filtering:** Filter expenses by category and date and view them within the context of the set budgets.
# - **Testing for Integrity:** The project includes comprehensive testing using Python's `unittest` framework to ensure each component works properly.

# #### **Future Enhancements:**
# - **Report Generation:** Automatic generation of reports (weekly/monthly) summarizing expenses and budgets.
# - **User Interface:** Potential future development could include a GUI for easier navigation and usage.
# - **Integration with External Tools:** The system could be expanded to integrate with external financial tracking tools or apps.

# This modular approach ensures flexibility and easy extension of functionalities in the future.