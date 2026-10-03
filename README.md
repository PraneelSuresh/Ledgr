# Ledgr 

A modern, local-first personal finance tracking application built with **Python**, **Flask**, and **Chart.js**. Effortlessly track income and expenses, organize transactions by category, and visualize spending habits—all stored locally on your device in structured CSV files with zero database setup required.

Available both as a standalone **Windows executable (.exe)** and a lightweight **Python web application**.

---

## Key Features

- **Interactive Web Dashboard**: Monitor total balance, monthly income, and monthly expenses at a glance with real-time color-coded cards and recent activity tables.
- **Transaction Management**: 
  - Add, edit, or delete transactions via a modal interface.
  - Automatic index re-sorting and ID management on updates and deletions.
- **Dynamic Timeframe & Category Filtering**: Filter transaction histories by timeframes (*This Week*, *This Month*, *All Time*) and transaction types (*Income*, *Expense*, *All Types*).
- **Visual Analytics**: Interactive bar charts (top spending categories) and doughnut charts (breakdown by *Needs*, *Wants*, *Savings*, *Investment*, and *Emergency*) powered by Chart.js.
- **Flexible Expense Classification**: Categorize entries into financial buckets (*Needs*, *Wants*, *Savings*, *Investment*, *Emergency*) to align with budgeting rules.
- **Persistent Local Data**: All data lives locally on your machine in `transactions.csv` and `filtered_transactions.csv`—keeping your financial records private.
- **Standalone Binary (.exe)**: Run as a native application without needing Python or external dependencies installed.

---

## Tech Stack

- **Backend**: Python 3, Flask, Jinja2 Templates
- **Frontend**: HTML5, CSS3 (Custom Dark Theme UI), JavaScript (ES6)
- **Data Visualization**: Chart.js (via CDN)
- **Local Storage**: Standard CSV & JSON File I/O
- **Packaging**: PyInstaller (for executable builds)

---

## Project Architecture

```
.
├── app.py                   # Main Flask application and web routing logic
├── csv_manager.py           # Core logic for CSV read/write, sorting, and analytics aggregation
├── Ledgr.spec               # PyInstaller build configuration file
├── static/
│   ├── script.js            # Frontend modal controls and Chart.js initialization
│   ├── style.css            # Modern dark-mode styling and responsive layouts
│   └── analytics.json       # Auto-generated runtime summary data
├── templates/
│   ├── index.html           # Main financial overview dashboard
│   ├── transactions.html    # Manage and filter transaction history
│   └── analytics.html       # Chart.js visualization page
└── transactions.csv         # Main user transaction dataset (auto-generated on runtime)
```

---

## Getting Started

### Option 1: Running the Executable (Recommended for End Users)

1. Download the latest `Ledgr.exe` from the **[Releases](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME/releases)** section.
2. Run `Ledgr.exe`.
3. Your default web browser will automatically launch `http://127.0.0.1:5000/`.
4. All data files (`transactions.csv`, `filtered_transactions.csv`, `static/analytics.json`) will be generated automatically in the directory where `Ledgr.exe` is located.

---

### Option 2: Running from Source (For Developers)

#### Prerequisites
- **Python 3.8+** installed on your machine.

#### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   cd YOUR_REPO_NAME
   ```

2. **Install dependencies:**
   ```bash
   pip install flask
   ```

3. **Run the Flask application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Building the Executable with PyInstaller

To bundle the application into a single `.exe` file using PyInstaller:

1. **Install PyInstaller:**
   ```bash
   pip install pyinstaller
   ```

2. **Build using the specification file:**
   ```bash
   pyinstaller Ledgr.spec
   ```

3. Find the generated `Ledgr.exe` inside the newly created `dist/` folder.

---

## Usage Guide

- **Dashboard**: Get an instant breakdown of net balance, total income, total expenses, and the 5 most recent transactions.
- **Add Transaction**: Click **+ Add Transaction** in the sidebar to record a new entry with type, date, category, expense classification, and description.
- **Edit / Delete**: Head to the **Transactions** page to filter entries, edit details, or delete unwanted records.
- **Analytics**: Visit the **Analytics** tab to view graphical charts illustrating where your money goes.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
