'''oops(object-oriented programming) concepts
class: A blueprint for creating objects
object: An instance of a class
abstraction: The process of hiding complex implementation details
inheritance: The mechanism of creating a new class based on an existing class
polymorphism: The ability of an object to take many forms'''
class car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start(self):
        print(f"{self.make} {self.model} is starting.")

    def stop(self):
        print(f"{self.make} {self.model} is stopping.")
my_car = car("Tata", "alto", 2020)
my_car.start()
my_car.stop()        