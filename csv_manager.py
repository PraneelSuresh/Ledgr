import csv
import tabulate


csv_headers = ['ID', 'Date', 'Type', 'Amount', 'Category', 'Expense Type', 'Description', 'Notes']
def save_transactions(transactions):
    with open("transactions.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers,)
        writer.writeheader()
        writer.writerows(transactions)


def load_transactions():
    transactions = []
    with open("transactions.csv", mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(row)
    return transactions


def get_transaction_id():
    counter = 0
    with open("transactions.csv") as file:
        reader = csv.reader(file)
        for _ in reader:
            counter +=1
    return counter


def sort_transactions(transactions):
    for _, item in enumerate(transactions):
        item["ID"] = int(item["ID"])
        item["ID"] = _+1
    return transactions