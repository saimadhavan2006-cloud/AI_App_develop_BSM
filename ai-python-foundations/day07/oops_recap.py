# OOP recap

# Class blueprint
class Shirt:
    def __init__(self, color, size, price):
        self.color = color
        self.size = size
        self.price = price


# Object creation
shirt1 = Shirt("black", "L", 300)
shirt2 = Shirt("orange", "XL", 450)

print(shirt1.color, shirt1.size, shirt1.price)
print(shirt2.color, shirt2.size, shirt2.price)


# Encapsulation
class ShirtEncapsulation:
    def __init__(self, price):
        self.__price = price

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if price > 20:
            self.__price = price
        else:
            print("Price must be greater than 20")


shirt3 = ShirtEncapsulation(900)
print(shirt3.get_price())
shirt3.set_price(950)
print(shirt3.get_price())


# Inheritance
class ShirtBase:
    def wear(self):
        print("Wearing shirt")


class FormalShirt(ShirtBase):
    def office(self):
        print("Suitable for office")


formal = FormalShirt()
formal.wear()
formal.office()


# Polymorphism
class Shirt:
    def wear(self):
        print("Wearing normal shirt")


class FormalShirt2(Shirt):
    def wear(self):
        print("Wearing formal shirt")


class Tshirt(Shirt):
    def wear(self):
        print("Wearing tshirt")


shirts = [FormalShirt2(), Tshirt()]
for shirt in shirts:
    shirt.wear()


# Abstraction
from abc import ABC, abstractmethod


class ShirtStore(ABC):
    def buy_shirt(self):
        self.check_inventory()
        self.process_payment()
        print("Shirt purchased")

    @abstractmethod
    def check_inventory(self):
        pass

    @abstractmethod
    def process_payment(self):
        pass


class MyShirtStore(ShirtStore):
    def check_inventory(self):
        print("Checking inventory")

    def process_payment(self):
        print("Processing payment")


store = MyShirtStore()
store.buy_shirt()