# Personal Finance Tracker

A lightweight, CLI-based financial management tool built in Python. Track daily transactions, manage spending categories, and gain clear insight into income, total expenses, and net balance—all saved locally in a structured CSV format.

---

## Key Features

* **Transaction Logging**: Easily record income and expenses with validated fields, including Date, Type, Category, Expense Type, Description, and Notes.
* **Automated Data Formatting**: Enforces valid date inputs (`YYYY-MM-DD`), transaction types (`Income` or `Expense`), and spending classifications (`Needs`, `Wants`, `Emergency`, `Savings`, `Investment`).
* **Transaction Management**: View formatted tabular records or delete transactions by ID with automatic index re-sorting.
* **Financial Overview**: Calculate total income, total expenses, and overall remaining balance in a unified view.
* **Category Breakdown**: Aggregate total expenditures across custom categories or uncategorized entries.
* **Persistent Local Storage**: Automatically saves all user data to a structured `transactions.csv` file without requiring an external database setup.

---

## Tech Stack

* **Language**: Python 3
* **Standard Modules**: `csv`, `datetime`, `sys`
* **Third-Party Libraries**: `tabulate` (for rendering ASCII tables in the terminal)

---

## File Architecture

* `main.py` - Entry point for the CLI application.
* `csv_manager.py` - Handles reading, writing, and sorting transaction records.
* `transactions.py` - Processing logic for balance calculation, categorization, and entry removal.
* `ui_and_input_handler.py` - Menu interface and command-line input validation.
* `transactions.csv` - Persistent dataset storage.

---

## Getting Started

### Prerequisites

Ensure Python 3.x is installed on your environment.

### Installation

1. Clone the repository or download the project files.
2. Install the required dependency:

```bash
pip install tabulate
```

### Running the Application
```bash
python main.py
```

### Usage Guide

1. Add Transaction: Prompts for required fields, validates input formats, assigns an ID, and appends the entry to `transactions.csv`.

2. Delete Transaction: Displays existing entries in tabular format and removes the specified ID while updating subsequent record indexes.

3. View Transactions: Outputs all logged transactions in an organized, readable table.

4. View Balance: Displays total income, total expenses, and remaining net balance.

5. Spending Summary: Summarizes expenses dynamically grouped by custom category names.

6. Exit: Safely closes the CLI application interface.
