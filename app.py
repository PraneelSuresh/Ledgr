import os
import sys
import webbrowser
import json
from datetime import date
from flask import Flask, render_template, request, redirect, url_for
import csv_manager

# Determine base path for bundled static files and templates
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(base_dir, 'templates')
static_folder = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='/static')

# Ensure working directory is set to where the executable resides for dynamic CSV/JSON files
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))

@app.route('/', methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        return redirect(url_for("dashboard"))

    transactions = csv_manager.load_transactions("transactions.csv")
    total_expenses, total_income = csv_manager.get_balance()
    return render_template('index.html', transactions=transactions, total_expenses=total_expenses, total_income=total_income)

@app.route('/transactions', methods=["GET", "POST"])
def transaction_page():
    chosen_timeframe = "all_time"
    chosen_type = "all"

    if request.method == "POST":
        action = request.form.get("action", "")
        chosen_timeframe = request.form.get("timeframe", "all_time")
        chosen_type = request.form.get("type", "all")

        if action == "save_transaction":
            transaction_id = request.form.get("transaction_id", "")
            transaction_type = request.form.get("transaction_type", "")
            transaction_amount = request.form.get("transaction_amount", 0)
            transaction_category = request.form.get("transaction_category", "")
            transaction_expense_type = request.form.get("transaction_expense_type", "")
            transaction_date = request.form.get("transaction_date", "")
            transaction_description = request.form.get("transaction_description", "")

            transactions = csv_manager.load_transactions("transactions.csv")

            if transaction_id != "":
                for transaction in transactions:
                    if int(transaction["ID"]) == int(transaction_id):
                        transaction["Type"] = transaction_type
                        transaction["Amount"] = transaction_amount
                        transaction["Category"] = transaction_category
                        transaction["Expense Type"] = transaction_expense_type
                        transaction["Date"] = transaction_date
                        transaction["Description"] = transaction_description
            else:
                new_id = csv_manager.get_transaction_id("transactions.csv")
                new_transaction = {
                    "ID": new_id,
                    "Date": transaction_date,
                    "Type": transaction_type,
                    "Amount": transaction_amount,
                    "Category": transaction_category,
                    "Expense Type": transaction_expense_type,
                    "Description": transaction_description
                }
                transactions.append(new_transaction)

            csv_manager.sort_transactions(transactions)
            csv_manager.save_transactions(transactions, "transactions.csv")
            return redirect(url_for("transaction_page"))

        elif "delete_transaction" in action:
            transactions = csv_manager.load_transactions("transactions.csv")
            transaction_to_be_deleted = int(action.split("_")[-1])
            new_transactions = [t for t in transactions if int(t["ID"]) != transaction_to_be_deleted]
            csv_manager.sort_transactions(new_transactions)
            csv_manager.save_transactions(new_transactions, "transactions.csv")
            return redirect(url_for("transaction_page"))

        all_transactions = csv_manager.load_transactions("transactions.csv")
        filtered_transactions = []

        if chosen_type.lower() == "income" and chosen_timeframe.lower() == "all_time":
            filtered_transactions = [t for t in all_transactions if t["Type"].lower() == "income"]
        elif chosen_type.lower() == "expense" and chosen_timeframe.lower() == "all_time":
            filtered_transactions = [t for t in all_transactions if t["Type"].lower() == "expense"]
        elif chosen_type.lower() == "all" and chosen_timeframe == "this_month":
            this_year, this_month = date.today().year, date.today().month
            for transaction in all_transactions:
                trans_date = date.fromisoformat(transaction["Date"])
                if trans_date.month == this_month and trans_date.year == this_year:
                    filtered_transactions.append(transaction)
        elif chosen_type.lower() == "income" and chosen_timeframe == "this_month":
            this_year, this_month = date.today().year, date.today().month
            for transaction in all_transactions:
                trans_date = date.fromisoformat(transaction["Date"])
                if trans_date.month == this_month and trans_date.year == this_year and transaction["Type"].lower() == "income":
                    filtered_transactions.append(transaction)
        elif chosen_type.lower() == "expense" and chosen_timeframe == "this_month":
            this_year, this_month = date.today().year, date.today().month
            for transaction in all_transactions:
                trans_date = date.fromisoformat(transaction["Date"])
                if trans_date.month == this_month and trans_date.year == this_year and transaction["Type"].lower() == "expense":
                    filtered_transactions.append(transaction)
        elif chosen_type.lower() == "all" and chosen_timeframe == "this_week":
            this_year, this_week = date.today().year, date.today().isocalendar().week
            for transaction in all_transactions:
                trans_date = date.fromisoformat(transaction["Date"])
                if trans_date.isocalendar()[1] == this_week and trans_date.year == this_year:
                    filtered_transactions.append(transaction)
        elif chosen_type.lower() == "income" and chosen_timeframe == "this_week":
            this_year, this_week = date.today().year, date.today().isocalendar().week
            for transaction in all_transactions:
                trans_date = date.fromisoformat(transaction["Date"])
                if trans_date.isocalendar()[1] == this_week and trans_date.year == this_year and transaction["Type"].lower() == "income":
                    filtered_transactions.append(transaction)
        elif chosen_type.lower() == "expense" and chosen_timeframe == "this_week":
            this_year, this_week = date.today().year, date.today().isocalendar().week
            for transaction in all_transactions:
                trans_date = date.fromisoformat(transaction["Date"])
                if trans_date.isocalendar()[1] == this_week and trans_date.year == this_year and transaction["Type"].lower() == "expense":
                    filtered_transactions.append(transaction)
        else:
            filtered_transactions = all_transactions

        csv_manager.save_transactions(filtered_transactions, "filtered_transactions.csv")

    if request.method == "GET":
        unfiltered_transactions = csv_manager.load_transactions("transactions.csv")
        csv_manager.save_transactions(unfiltered_transactions, "filtered_transactions.csv")

    filtered_transactions = csv_manager.load_transactions("filtered_transactions.csv")
    return render_template('transactions.html', filtered_transactions=filtered_transactions, chosen_timeframe=chosen_timeframe, chosen_type=chosen_type)

@app.route('/analytics', methods=["GET", "POST"])
def analytics():
    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "save_transaction":
            transaction_id = request.form.get("transaction_id", "")
            transaction_type = request.form.get("transaction_type", "")
            transaction_amount = request.form.get("transaction_amount", 0)
            transaction_category = request.form.get("transaction_category", "")
            transaction_expense_type = request.form.get("transaction_expense_type", "")
            transaction_date = request.form.get("transaction_date", "")
            transaction_description = request.form.get("transaction_description", "")

            transactions = csv_manager.load_transactions("transactions.csv")

            if transaction_id != "":
                for transaction in transactions:
                    if int(transaction["ID"]) == int(transaction_id):
                        transaction["Type"] = transaction_type
                        transaction["Amount"] = transaction_amount
                        transaction["Category"] = transaction_category
                        transaction["Expense Type"] = transaction_expense_type
                        transaction["Date"] = transaction_date
                        transaction["Description"] = transaction_description
            else:
                new_id = csv_manager.get_transaction_id("transactions.csv")
                new_transaction = {
                    "ID": new_id,
                    "Date": transaction_date,
                    "Type": transaction_type,
                    "Amount": transaction_amount,
                    "Category": transaction_category,
                    "Expense Type": transaction_expense_type,
                    "Description": transaction_description
                }
                transactions.append(new_transaction)

            csv_manager.sort_transactions(transactions)
            csv_manager.save_transactions(transactions, "transactions.csv")

        # Write analytics.json to the static folder path
        analytics_file = os.path.join("static", "analytics.json")
        os.makedirs(os.path.dirname(analytics_file), exist_ok=True)
        with open(analytics_file, "w") as analytics_json:
            combined_analytics = {
                "expense_type_summary": csv_manager.group_by_expense_type(),
                "category_summary": csv_manager.categorize_transactions()
            }
            json.dump(combined_analytics, analytics_json, indent=4)

        return redirect(url_for("analytics"))

    analytics_file = os.path.join("static", "analytics.json")
    os.makedirs(os.path.dirname(analytics_file), exist_ok=True)
    with open(analytics_file, "w") as analytics_json:
        combined_analytics = {
            "expense_type_summary": csv_manager.group_by_expense_type(),
            "category_summary": csv_manager.categorize_transactions()
        }
        json.dump(combined_analytics, analytics_json, indent=4)

    transactions = csv_manager.load_transactions("transactions.csv")
    return render_template('analytics.html', transactions=transactions)

if __name__ == '__main__':
    webbrowser.open_new("http://127.0.0.1:5000/")
    app.run(host="127.0.0.1", port=5000, debug=False)