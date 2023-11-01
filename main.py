import os
import datetime
# Initialize the BankData.txt file if it doesn't exist
try:
    with open("BankData.txt", "x") as bank_data_file:
        bank_data_file.write("0.0")
except FileExistsError:
    pass

# Initialize the TransactionLog.txt file if it doesn't exist
try:
    with open("TransactionLog.txt", "x") as transaction_log_file:
        transaction_log_file.write("Transaction Log:\n")
except FileExistsError:
    pass

# Function to check the current balance for a specific user
def check_balance(username):
    user_data = load_user_data()
    return user_data.get(username, {"balance": 0.0})["balance"]

# Function to make a deposit
def make_deposit(username, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid deposit amount.")
        else:
            user_data = load_user_data()
            current_balance = user_data.get(username, {"balance": 0.0})["balance"]
            current_balance += amount
            user_data[username] = {"password": user_data[username]["password"], "balance": current_balance}
            save_user_data(user_data)
            now = datetime.datetime.now()
            transaction_time = now.strftime("%Y-%m-%d %H:%M:%S")
            with open("TransactionLog.txt", "a") as transaction_log_file:
                transaction_log_file.write(f"{username} deposited: +${amount} at {transaction_time}\n")
            print(f"Deposited ${amount}. Current balance: ${current_balance}")
    except ValueError:
        print("Invalid input. Please enter a valid deposit amount.")
# Function to make a withdrawal
def make_withdrawal(username, amount):
    try:
        amount = float(amount)
        if amount <= 0:
            print("Invalid withdrawal amount.")
        else:
            user_data = load_user_data()
            current_balance = user_data.get(username, {"balance": 0.0})["balance"]
            if current_balance >= amount:
                current_balance -= amount
                user_data[username] = {"password": user_data[username]["password"], "balance": current_balance}
                save_user_data(user_data)
                now = datetime.datetime.now()
                transaction_time = now.strftime("%Y-%m-%d %H:%M:%S")
                with open("TransactionLog.txt", "a") as transaction_log_file:
                    transaction_log_file.write(f"{username} withdrew: -${amount} at {transaction_time}\n")
                print(f"Withdrew ${amount}. Current balance: ${current_balance}")
            else:
                print("Insufficient funds.")
    except ValueError:
        print("Invalid input. Please enter a valid withdrawal amount.")
# Function to load user data from the file
def load_user_data():
    user_data = {}
    with open("UserData.txt", "r") as user_data_file:
        for line in user_data_file:
            username, password, balance = line.strip().split(":")
            user_data[username] = {"password": password, "balance": float(balance)}
    return user_data

# Function to save user data to the file
def save_user_data(user_data):
    with open("UserData.txt", "w") as user_data_file:
        for username, data in user_data.items():
            user_data_file.write(f"{username}:{data['password']}:{data['balance']}\n")

  # Function to create a new user account
def create_account():
    user_data = load_user_data()
    while True:
        username = input("Enter a username: ").strip().lower()

        if not username:
            print("Username cannot be empty. Please enter a valid username.")
        elif username in user_data:
            print("Username already exists. Please choose a different one.")
        else:
            break

    while True:
        password = input("Create a password: ").strip()
        verify_password = input("Verify your password: ").strip()

        if not password:
            print("Password cannot be empty. Please enter a valid password.")
        elif password == verify_password:
            user_data[username] = {"password": password, "balance": 0.0}
            save_user_data(user_data)
            print("Account created successfully.")
            break
        else:
            print("Password verification failed. Please try again.")



# Function to authenticate the user
def login():
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    user_data = load_user_data()

    if username in user_data and user_data[username]["password"] == password:
        return username
    return None

# Create an account or log in
while True:
    print("Would you like to create an account or log in? (Create/Login/Exit)")
    action = input().strip().lower()
    if action == "create":
        create_account()
    elif action == "login":
        username = login()
        if username:
            print(f"Login successful, {username}.")
            break
        else:
            print("Invalid username or password. Please try again or create an account.")
    elif action == "exit":
        print("Goodbye!")
        exit()
    else:
        print("Invalid input. Please enter 'Create', 'Login', or 'Exit'.")

# Rest of the banking application code (deposit/withdraw) can go here.
while True:
    print("Would you like to make a transaction? (Yes or No)")
    choice = input().strip().lower()

    if choice == "no":
        print("Goodbye!")
        break
    elif choice == "yes":
        print("Would you like to make a deposit or withdrawal? (Deposit or Withdraw)")
        transaction_choice = input().strip().lower()

        if transaction_choice == "deposit":
            print(f"Current balance: ${check_balance(username)}")
            print("How much would you like to deposit?")
            amount = input().strip()
            make_deposit(username, amount)
        elif transaction_choice == "withdraw":
            print(f"Current balance: ${check_balance(username)}")
            print("How much would you like to withdraw?")
            amount = input().strip()
            make_withdrawal(username, amount)
        else:
            print("Invalid input. Please enter 'Deposit' or 'Withdraw'.")
    else:
        print("Invalid input. Please enter 'Yes' or 'No'.")

