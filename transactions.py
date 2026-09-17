import csv_manager
import ui_and_input_handler
import tabulate

def add_transaction():
    transactions = csv_manager.load_transactions()
    new_transaction = ui_and_input_handler.create_new_transaction()
    transactions.append(new_transaction)
    print("Adding transaction...")
    csv_manager.save_transactions(transactions)

def delete_transaction():
    transactions = csv_manager.load_transactions()
    print(tabulate.tabulate(transactions, headers="keys"))
    print("Enter the ID of the transaction that you want to delete")
    while True:
        deleted_transaction = input("Transaction ID: ")
        try:
            deleted_transaction = int(deleted_transaction)
        except ValueError :
            print("Invalid ID")
        else:
            if 1 <= deleted_transaction <= len(transactions):
                transactions.pop(deleted_transaction-1)
                print("Deleting transaction...")
                print("Transaction deleted")
                return transactions
            else:
                print("The transaction you are trying to delete is not in the list of transactions.")

def get_balance():
    total_income = 0
    total_expenses = 0
    transactions = csv_manager.load_transactions()
    for transaction in transactions:
        if transaction["Type"] == "income":
            transaction["Amount"] = int(transaction["Amount"])
            total_income += transaction["Amount"]
        else:
            transaction["Amount"] = int(transaction["Amount"])
            total_expenses += transaction["Amount"]
    return total_expenses, total_income


def categorize_transactions():
    transactions = csv_manager.load_transactions()
    categories = set()
    category_sum = {"Uncategorized" : 0}
    tabulated_category_summary = {"Category": [], "Amount": []}
    for transaction in transactions:
        if transaction["Category"] != "":
            categories.add(transaction["Category"])
    for category in categories:
        category_sum.update({category: 0})
    for transaction in transactions:
        if transaction["Category"] == "":
            category_sum["Uncategorized"] += int(transaction["Amount"])
        else:
            transaction_category = transaction["Category"]
            category_sum[transaction_category] += int(transaction["Amount"])
    for category, amount in category_sum.items():
        tabulated_category_summary["Category"].append(category)
        tabulated_category_summary["Amount"].append(amount)
    return tabulated_category_summary