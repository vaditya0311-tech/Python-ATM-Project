# Python ATM Project

A simple terminal-based ATM application developed using Python.

## Project Structure

Python_ATM_Project/
│
├── account.py
├── atm_core.py
├── main.py
└── README.md

## Features

- Create a new bank account
- Four-digit PIN authentication
- Login and logout
- Check account balance
- Deposit money
- Withdraw money
- Transfer money between accounts
- View transaction history
- Save account information using JSON

## Requirements

- Python 3.8 or higher

No external Python packages are required.

## How to Run

1. Open the project folder.
2. Open a terminal in that folder.
3. Run the following command:

   python main.py

## Data Storage

Account information is automatically stored in:

accounts.json

This file is created when the application saves account data.

## Modules

### account.py
Contains the Account class and account operations.

### atm_core.py
Contains the ATM class, account management,
authentication, data storage, and money transfers.

### main.py
Contains the terminal interface and application entry point.

## Important Security Note

This is an educational project, not a real banking system.
PINs are stored as plain text in the JSON file.
Do not use real banking credentials or real money.