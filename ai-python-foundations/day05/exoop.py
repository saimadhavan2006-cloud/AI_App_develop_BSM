class car:
    def start(self):
        print("Car engine is starting.")
class BMW(car):
    def start(self):
        print("BMW engine is starting with a roar!")    
class tesla(car):
    def start(self):
        print("Tesla engine is starting silently!")
class audi(car):
    def start(self):
        print("Audi engine is starting with a smooth sound!")        
class bike:
    def start(self):
        print("Bike engine is starting.")    
tesla = tesla()
bmw = BMW() 
audi = audi()
bike = bike()
tesla.start()  # Output: Tesla engine is starting silently!
bmw.start()    # Output: BMW engine is starting with a roar!
audi.start()   # Output: Audi engine is starting with a smooth sound!
bike.start()   # Output: Bike engine is starting.