import sys
import transactions
import datetime
import csv_manager
import tabulate

def main_menu():
    header = 30 * "="
    print(header)
    print("Personal Finance Tracker".center(20, "="))
    print(header)
    print("""
    1. Add Transaction
    2. Delete Transaction
    3. View Transactions
    4. View Balance
    5. Spending Summary
    6. Exit
    """)
    print(header)


def menu_select():
        while True:
            menu_input = input("Input: ").strip()
            if menu_input == "1":
                transactions.add_transaction()
                break
            elif menu_input == "2":
                updated_transactions = transactions.delete_transaction()
                sorted_updated_transactions = csv_manager.sort_transactions(updated_transactions)
                csv_manager.save_transactions(sorted_updated_transactions)
                break
            elif menu_input == "3":
                transactions_ = csv_manager.load_transactions()
                print(tabulate.tabulate(transactions_, headers="keys"))
                break                
            elif menu_input == "4":
                total_expenses, total_income = transactions.get_balance()
                print(tabulate.tabulate([["Total Income", "Total Expenses", "Balance"], [total_income, total_expenses, total_income-total_expenses]],headers="firstrow"))
                break
            elif menu_input == "5":
                category_summary = transactions.categorize_transactions()
                print(tabulate.tabulate(category_summary, headers=["Category", "Amount"]))
                break
            elif menu_input == "6":
                print("Exiting program...")
                sys.exit()
            else:
                print("Invalid input, choose one of the options from the given list")


def create_new_transaction():
    transaction_id = csv_manager.get_transaction_id()
    print("Enter transaction date (YYYY-MM-DD)")
    while True:
        transaction_date = input("Enter Date: ").strip()
        try:
            datetime.date.fromisoformat(transaction_date)
        except ValueError:
            print("Invalid date format. Try again")
        else:
            break
    print("Enter transaction type (Income/Expense)")
    while True:
        transaction_type = input("Enter Type: ").capitalize()
        if transaction_type == "Income" or transaction_type == "Expense":
            break
        else:
            print("Invalid type. Try again")
    print("Enter transaction amount")
    while True:
        transaction_amount = input("Enter Amount: ").strip()
        try:
            transaction_amount = float(transaction_amount)
        except ValueError:
            print("Invalid amount. Try again")
        else:
            transaction_amount = int(transaction_amount)
            break
    if transaction_type == "Expense":
        print("Enter expense type (Needs/Wants/Emergency/Savings/Investment)")
        while True:
            transaction_expense_type = input("Enter Expense Type: ").capitalize().strip()
            if transaction_expense_type in ['Needs', 'Wants', 'Emergency', 'Savings', 'Investment']:
                break
            else:
                print("Invalid expense type. Try again")
    else:
        transaction_expense_type = ""
    print("Enter Transaction Category")
    transaction_category = input("Enter Category: ").capitalize().strip()
    print("Enter Transaction Description (Optional)")
    transaction_description = input("Enter Transaction Description: ").strip()
    print("Enter Transaction Notes (Optional)")
    transaction_notes = input("Enter Transaction Notes: ").strip()

    new_transaction = {
        "ID": transaction_id,
        "Date": transaction_date,
        "Type": transaction_type,
        "Amount": transaction_amount,
        "Category": transaction_category,
        "Expense Type": transaction_expense_type,
        "Description": transaction_description,
        "Notes": transaction_notes
    }

    return new_transaction