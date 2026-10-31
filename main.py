from getpass import getpass

from atm_core import ATM


def atm_menu(atm):
    """Menu displayed after successful login."""

    while True:
        print("\n" + "=" * 50)
        print("ATM MENU".center(50))
        print("=" * 50)
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Logout")
        print("-" * 50)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            balance = atm.get_balance()
            print(f"\nCurrent Balance: ${balance:.2f}")

        elif choice == "2":
            try:
                amount = float(input("Enter deposit amount: $"))

                if atm.deposit(amount):
                    print("Deposit successful!")
                    print(f"New balance: ${atm.get_balance():.2f}")
                else:
                    print("Invalid deposit amount.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            try:
                amount = float(input("Enter withdrawal amount: $"))

                if atm.withdraw(amount):
                    print("Withdrawal successful!")
                    print(f"New balance: ${atm.get_balance():.2f}")
                else:
                    print("Invalid amount or insufficient balance.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            target = input("Enter receiver account number: ").strip()

            try:
                amount = float(input("Enter transfer amount: $"))

                if atm.transfer(target, amount):
                    print("Transfer successful!")
                    print(f"New balance: ${atm.get_balance():.2f}")
                else:
                    print("Transfer failed. Check account and amount.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            transactions = atm.get_transactions(limit=20)

            print("\n" + "=" * 50)
            print("TRANSACTION HISTORY".center(50))
            print("=" * 50)

            if not transactions:
                print("No transactions available.")
            else:
                for index, transaction in enumerate(
                    reversed(transactions), 1
                ):
                    timestamp = transaction["timestamp"]
                    timestamp = timestamp[:19].replace("T", " ")

                    amount = transaction["amount"]

                    print(f"\n{index}. {timestamp}")
                    print(f"Type: {transaction['type']}")
                    print(f"Amount: ${amount:.2f}")
                    print(f"Balance: ${transaction['balance']:.2f}")
                    print(f"Description: {transaction['description']}")

        elif choice == "6":
            atm.logout()
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


def atm_interface():
    """Main ATM application interface."""

    atm = ATM()

    while True:
        print("\n" + "=" * 50)
        print("WELCOME TO PYTHON ATM".center(50))
        print("=" * 50)
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        print("-" * 50)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print("\nLOGIN")
            account_number = input("Enter account number: ").strip()
            pin = getpass("Enter PIN: ")

            if atm.login(account_number, pin):
                print("\nLogin successful!")
                atm_menu(atm)
            else:
                print("\nInvalid account number or PIN.")

        elif choice == "2":
            print("\nCREATE ACCOUNT")

            pin = getpass("Create a 4-digit PIN: ")

            if not pin.isdigit() or len(pin) != 4:
                print("PIN must contain exactly 4 digits.")
                continue

            try:
                initial_deposit = float(
                    input("Enter initial deposit amount: $")
                )

                account_number = atm.create_account(
                    pin, initial_deposit
                )

                print("\nAccount created successfully!")
                print(f"Your account number: {account_number}")
                print("Please keep your account number safe.")

            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "3":
            print("\nThank you for using Python ATM!")
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    atm_interface()