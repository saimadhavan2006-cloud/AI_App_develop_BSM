class bankAccount:
    def __init__(self, bal):
        self.__bal = bal

    def deposit(self, amount):
        if amount > 0:
            self.__bal += amount
            print(f"Money Deposited {amount}.")
        else:
            print("Deposit amount must be positive.")
    def withdraw(self, amount):
        if amount <= self.__bal:
            self.__bal -= amount
            print(f"Money Withdrew {amount}.")
        else:
            print("Insufficient funds.")
    def check_balance(self):
        print(f"Current balance: {self.__bal}")                    
acc1 = bankAccount(1000)
acc1.deposit(2000)
acc1.withdraw(250)  
acc1.check_balance()  # Output: Current balance:
        
