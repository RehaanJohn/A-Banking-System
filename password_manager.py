import hashlib
import getpass
import csv
import random

class BankSystem:
    def __init__(self):
        self.password_manager = {}
    
    def generate_account_number(self):
        # Generate a random account number (e.g., a 10-digit number)
        return random.randint(1000000000, 9999999999)

    def main_menu(self, username):
        while True:
            ch = int(input("Options\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Export account as csv file\n 5. Logout\nEnter choice: "))
            if ch == 1:
                self.deposit(username)
            elif ch == 2:
                if self.password_manager[username]['balance'] == 0:
                    print("You cannot withdraw as you have no balance in your account")
                    self.main_menu(username)
                else:
                    self.withdraw(username)
            elif ch == 3:
                print(f"Your current Bank Balance is: ${self.password_manager[username]['balance']}")
            elif ch == 4:
                self.export_account_data(username)
            elif ch == 5:
                print(f"Logging out {username}...\n")
                break
            else:
                print("Invalid choice, please try again.")
    
    def export_account_data(self, username):
        filename = f"{username}_account_data.csv"
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Balance'])
            writer.writerow([username, self.password_manager[username]['balance']])
        
        print(f"Account data has been exported to {filename}")

    def deposit(self, username):
        dep = float(input("Choose amount to be deposited: $"))
        if dep <= 0:
            print("Deposit amount must be greater than zero!")
            return
        elif dep > 50000:
            print("Deposit amount cannot be greater than $50,000!")
            return
        else:
            self.password_manager[username]['balance'] += dep
            print(f"An amount of ${dep} has been deposited to your bank account!")

    def withdraw(self, username):
         w = float(input("Choose amount to withdraw: $"))
         if w <= 0:
            print("Withdrawal amount must be greater than zero!")
            return
         if w > self.password_manager[username]['balance']:
            print("Insufficient balance!")
         else:
            self.password_manager[username]['balance'] -= w
            print(f"An amount of ${w} has been withdrawn from your bank account!")

    def register(self):
        username = input("Enter username: ")
        if len(username) < 7:
            print("Username must be longer than 7 characters!")
            return self.register()

        elif username in self.password_manager:
            print("Username already taken. Please choose another one!")
            return self.register()

        password = getpass.getpass("Enter password: ")
        if len(password) < 7:
            print("Password must be longer than 7 characters!")
            return self.register()

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        # Generate account number
        account_number = self.generate_account_number()
        
        # Ask for a 4-digit PIN
        pin = input("Enter a 4-digit PIN: ")
        while not (pin.isdigit() and len(pin) == 4):
            print("PIN must be a 4-digit integer!")
            pin = input("Enter a 4-digit PIN: ")

        # Set initial balance to 0 for the new user
        self.password_manager[username] = {
            'password': hashed_password,
            'balance': 0,
            'account_number': account_number,
            'pin': pin
        }
        print("Account created successfully!")

    def login(self):
        username = input("Enter your username: ")
        if username not in self.password_manager:
            print("Username not found!")
            return

        password = getpass.getpass("Enter password: ")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if self.password_manager[username]['password'] == hashed_password:
            print("Login successful!")
            self.main_menu(username)
        else:
            print("Invalid login attempt!")

    def main(self):
        while True:
            choice = input("1. Register\n2. Login\n3. Exit\nEnter choice: ")
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                break
            else:
                print("Invalid choice! Please try again.")

if __name__ == "__main__":
    bank_system = BankSystem()
    bank_system.main()







