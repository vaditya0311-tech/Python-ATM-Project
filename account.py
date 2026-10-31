from datetime import datetime
from math import isfinite


class Account:
    """Bank account and its transaction history."""

    def __init__(
        self,
        account_number,
        pin,
        balance=0.0,
        transactions=None,
        created_at=None,
    ):
        self.account_number = str(account_number)
        self.pin = str(pin)
        self.balance = float(balance)
        self.transactions = transactions or []
        self.created_at = created_at or datetime.now().isoformat()

    def add_transaction(self, transaction_type, amount, description=""):
        self.transactions.append(
            {
                "type": transaction_type,
                "amount": amount,
                "balance": self.balance,
                "description": description,
                "timestamp": datetime.now().isoformat(),
            }
        )

    def deposit(self, amount):
        if not isfinite(amount) or amount <= 0:
            return False

        self.balance += amount
        self.add_transaction(
            "DEPOSIT", amount, f"Deposited ${amount:.2f}"
        )
        return True

    def withdraw(self, amount):
        if not isfinite(amount) or amount <= 0 or amount > self.balance:
            return False

        self.balance -= amount
        self.add_transaction(
            "WITHDRAWAL", -amount, f"Withdrew ${amount:.2f}"
        )
        return True

    def get_balance(self):
        return self.balance

    def get_transactions(self, limit=10):
        if limit <= 0:
            return []
        return self.transactions[-limit:]
