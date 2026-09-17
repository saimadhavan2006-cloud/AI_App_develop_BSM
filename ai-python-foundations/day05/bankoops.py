from datetime import datetime
class BankAccount:
    def __init__(self, account_holder, balance=0):        
        self.acc_holder = account_holder
        self.bal = balance

    def get_transaction_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")    

    def deposit(self, amount):
        if amount > 0:
            self.bal += amount
            print(f"Money Deposited {amount}. ")
            print(f"Transaction time: {self.get_transaction_time()}")
        else:
            print("Deposit amount must be positive.")


    def withdraw(self, amount):
        if 0 < amount <= self.bal:
            self.bal -= amount
            print(f"Money Withdrew {amount}.")
            print(f"Transaction time: {self.get_transaction_time()}")
        else:
            print("Insufficient funds.")

    def check_balance(self):
        print(f"account holder: {self.acc_holder},\n Balance: {self.bal}")

acc1 = BankAccount("Maddy", 1000)
acc1.check_balance()
acc1.deposit(2000) 
acc1.check_balance()
acc1.withdraw(250)
acc1.check_balance()       