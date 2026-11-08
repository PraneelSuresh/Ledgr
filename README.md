# Ledgr

A local-first, privacy-focused personal finance tracker built with Django.

Originally started as a Python CLI application (v1.0.0) and later refactored into a full-stack web application.

<img width="1917" height="998" alt="image" src="https://github.com/user-attachments/assets/15390d1d-4004-4218-8b59-52525f464a37" />

## About The Project

Most finance apps store your sensitive financial data on their servers and charge a monthly subscription. Ledgr is different. It runs entirely on your local machine. Your data never leaves your computer.

This project demonstrates a complete backend-to-frontend pipeline, including secure user authentication, relational database design, complex data aggregation, and responsive UI design.

## Features

- Multi-Account Management: Track bank accounts, cash, and credit cards.
- Transaction Tracking: Log income and expenses with detailed categorization.
- Zero-Based Budgeting: Organize expenses into buckets (Needs, Wants, Savings, Investment).
- Data Visualization: A dynamic dashboard using Chart.js to view monthly income vs. expenses and category breakdowns.
- Secure Authentication: User registration, login, and strict data isolation (users can only view their own data).
- Comprehensive Testing: A full Pytest suite covering security vulnerabilities (ownership isolation) and model validation rules.

## Tech Stack

- Backend: Python 3.12, Django 5.x
- Database: SQLite (local-first)
- Frontend: HTML5, Custom CSS (Glassmorphism/Dark theme), Vanilla JavaScript
- Data Viz: Chart.js
- Testing: Pytest, pytest-django

## Getting Started (Local Development)

To get a local copy up and running, follow these simple steps.

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository
```
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```
On macOS/Linux, use: source .venv/bin/activate

3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run database migrations
```bash
python manage.py migrate
```
5. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```
6. Start the development server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

## Running the Tests

Ledgr uses pytest to ensure data integrity and security. To run the test suite:

pytest

The tests cover:
- Security: Proving that User B cannot edit or delete User A's transactions.
- Validation: Proving that expenses require a bucket, and incomes cannot have a bucket.

## Installation (Windows Executable)

Currently Unavailable

For non-developers, you can download the standalone Windows installer from the Releases tab on the right.

## Project Evolution

- v1.0.0: Initial Python CLI version.
- v2.0.0: CLI version built with the blessed library for an interactive terminal UI.
- v3.0.0 (Current): Full Django Web Application.
