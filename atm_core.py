import json
import os
import secrets
from math import isfinite

from account import Account


class ATM:
    """Manage accounts, authentication, and ATM transactions."""

    def __init__(self, data_file="accounts.json"):
        self.data_file = data_file
        self.accounts = {}
        self.current_account = None
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            return

        with open(self.data_file, "r", encoding="utf-8") as data_file:
            data = json.load(data_file)

        if not isinstance(data, dict):
            raise ValueError("Account data must be a JSON object.")

        for account_number, account_data in data.items():
            self.accounts[account_number] = Account(
                account_number=account_data["account_number"],
                pin=account_data["pin"],
                balance=account_data.get("balance", 0.0),
                transactions=account_data.get("transactions", []),
                created_at=account_data.get("created_at"),
            )

    def save_data(self):
        data = {
            account_number: {
                "account_number": account.account_number,
                "pin": account.pin,
                "balance": account.balance,
                "transactions": account.transactions,
                "created_at": account.created_at,
            }
            for account_number, account in self.accounts.items()
        }

        with open(self.data_file, "w", encoding="utf-8") as data_file:
            json.dump(data, data_file, indent=2)

    def create_account(self, pin, initial_deposit=0.0):
        pin = str(pin)
        if len(pin) != 4 or not pin.isdigit():
            raise ValueError("PIN must contain exactly 4 digits.")
        if not isfinite(initial_deposit) or initial_deposit < 0:
            raise ValueError("Initial deposit must be a non-negative amount.")

        account_number = str(secrets.randbelow(9000000000) + 1000000000)
        while account_number in self.accounts:
            account_number = str(secrets.randbelow(9000000000) + 1000000000)

        account = Account(account_number, pin, initial_deposit)
        if initial_deposit > 0:
            account.add_transaction(
                "DEPOSIT",
                initial_deposit,
                f"Initial deposit of ${initial_deposit:.2f}",
            )
        self.accounts[account_number] = account
        self.save_data()
        return account_number

    def login(self, account_number, pin):
        account = self.accounts.get(str(account_number))
        if account is None or account.pin != str(pin):
            return False

        self.current_account = account
        return True

    def logout(self):
        self.current_account = None

    def _require_login(self):
        if self.current_account is None:
            raise RuntimeError("Log in before using account operations.")
        return self.current_account

    def get_balance(self):
        return self._require_login().get_balance()

    def deposit(self, amount):
        account = self._require_login()
        if not account.deposit(amount):
            return False
        self.save_data()
        return True

    def withdraw(self, amount):
        account = self._require_login()
        if not account.withdraw(amount):
            return False
        self.save_data()
        return True

    def transfer(self, target_account_number, amount):
        sender = self._require_login()
        receiver = self.accounts.get(str(target_account_number))
        if (
            receiver is None
            or receiver is sender
            or not isfinite(amount)
            or amount <= 0
            or amount > sender.balance
        ):
            return False

        sender.balance -= amount
        sender.add_transaction(
            "TRANSFER",
            -amount,
            f"Transferred ${amount:.2f} to {receiver.account_number}",
        )
        receiver.balance += amount
        receiver.add_transaction(
            "TRANSFER",
            amount,
            f"Received ${amount:.2f} from {sender.account_number}",
        )
        self.save_data()
        return True

    def get_transactions(self, limit=10):
        return self._require_login().get_transactions(limit)
