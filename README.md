# Personal Finance Tracker

A lightweight, CLI-based financial management tool built in Python[cite: 1, 2]. Track daily transactions, manage spending categories, and gain clear insight into income, total expenses, and net balance—all saved locally in a structured CSV format.

---

## Key Features

* **Transaction Logging**: Easily record income and expenses with validated fields, including Date, Type, Category, Expense Type, Description, and Notes.
* **Automated Data Formatting**: Enforces valid date inputs (`YYYY-MM-DD`), transaction types (`Income` or `Expense`), and spending classifications (`Needs`, `Wants`, `Emergency`, `Savings`, `Investment`)[cite: 4].
* **Transaction Management**: View formatted tabular records or delete transactions by ID with automatic index re-sorting.
* **Financial Overview**: Calculate total income, total expenses, and overall remaining balance in a unified view.
* **Category Breakdown**: Aggregate total expenditures across custom categories or uncategorized entries.
* **Persistent Local Storage**: Automatically saves all user data to a structured `transactions.csv` file without requiring an external database setup[cite: 1, 3, 4].

---

## Tech Stack

* **Language**: Python 3[cite: 1, 2]
* **Standard Modules**: `csv`[cite: 1], `datetime`[cite: 4], `sys`[cite: 4]
* **Third-Party Libraries**: `tabulate` (for rendering ASCII tables in the terminal)[cite: 1, 3, 4]

---

## File Architecture

* `main.py` - Entry point for the CLI application[cite: 2].
* `csv_manager.py` - Handles reading, writing, and sorting transaction records[cite: 1].
* `transactions.py` - Processing logic for balance calculation, categorization, and entry removal[cite: 3].
* `ui_and_input_handler.py` - Menu interface and command-line input validation[cite: 4].
* `transactions.csv` - Persistent dataset storage[cite: 1, 3, 4].

---

## Getting Started

### Prerequisites

Ensure Python 3.x is installed on your environment.

### Installation

1. Clone the repository or download the project files.
2. Install the required dependency:

```bash
pip install tabulate
