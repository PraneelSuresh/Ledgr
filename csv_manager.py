import csv
import os

csv_headers = ['ID', 'Date', 'Type', 'Amount', 'Category', 'Expense Type', 'Description']

def save_transactions(transactions, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(transactions)

def load_transactions(filename):
    if not os.path.exists(filename):
        return []
    transactions = []
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)
    return transactions

def get_transaction_id(filename):
    counter = 0
    with open(filename) as file:
        reader = csv.reader(file)
        for row in reader:
            counter += 1
    return counter

def sort_transactions(transactions):
    for index, transaction in enumerate(transactions):
        transaction["ID"] = index + 1
    return transactions

def get_balance():
    total_income = 0.0
    total_expenses = 0.0
    transactions = load_transactions("transactions.csv")
    for transaction in transactions:
        if transaction["Type"].lower() == "income":
            total_income += float(transaction["Amount"])
        else:
            total_expenses += float(transaction["Amount"])
    return total_expenses, total_income

def group_by_expense_type():
    transactions = load_transactions("transactions.csv")
    expense_types = ["Needs", "Wants", "Savings", "Investments"]
    expense_type_totals = []
    expense_type_summary = {}
    needs_total = 0.0
    wants_total = 0.0
    savings_total = 0.0
    investments_total = 0.0
    for transaction in transactions:
        if transaction["Type"].lower() == "expense":
            expense_type = transaction["Expense Type"].lower()
            if expense_type == "needs":
                needs_total += float(transaction["Amount"])
            elif expense_type == "wants":
                wants_total += float(transaction["Amount"])
            elif expense_type == "savings":
                savings_total += float(transaction["Amount"])
            elif expense_type == "investment" or expense_type == "investments":
                investments_total += float(transaction["Amount"])
    expense_type_totals.append(needs_total)
    expense_type_totals.append(wants_total)
    expense_type_totals.append(savings_total)
    expense_type_totals.append(investments_total)
    expense_type_summary["Expense Type"] = expense_types
    expense_type_summary["Expense Type Totals"] = expense_type_totals
    return expense_type_summary 

def categorize_transactions():
    transactions = load_transactions("transactions.csv")
    categories = set()
    category_sum = {"Uncategorized": 0.0}
    tabulated_category_summary = {"Category": [], "Amount": []}
    
    for transaction in transactions:
        if transaction["Type"].lower() == "expense":
            if transaction["Category"] != "":
                categories.add(transaction["Category"])
                
    for category in categories:
        category_sum[category] = 0.0
        
    for transaction in transactions:
        if transaction["Type"].lower() == "expense":
            if transaction["Category"] == "":
                category_sum["Uncategorized"] += float(transaction["Amount"])
            else:
                transaction_category = transaction["Category"]
                category_sum[transaction_category] += float(transaction["Amount"])
                
    for category, amount in category_sum.items():
        tabulated_category_summary["Category"].append(category)
        tabulated_category_summary["Amount"].append(amount)
        
    return tabulated_category_summary