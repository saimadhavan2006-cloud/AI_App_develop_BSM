from abc import ABC, abstractmethod
class BankAcc(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

   


class SavingsAccount(BankAcc):
    def __init__(self, acc_holder, balance=0):
        self.acc_holder = acc_holder
        self.bal = balance

    def deposit(self, amount):
        if amount > 0:
            self.bal += amount
            print(f"Money Deposited {amount}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= self.bal:
            self.bal -= amount
            print(f"Money Withdrew {amount}.")
        else:
            print("Insufficient funds.")


acc1 = SavingsAccount("Madhu", 1000)
acc1.deposit(2000)
acc1.withdraw(250)  
print(f"Current balance: {acc1.bal}")
