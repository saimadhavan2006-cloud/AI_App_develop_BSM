class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclasses must implement this method")

class Dog(Animal):
    def speak(self):
        print(f"{self.name} says Woof!")

class Cat(Animal):
    def speak(self):
        print(f"{self.name} says Meow!")        

cat = Cat("Whiskers")
dog = Dog("Buddy")        
cat.speak()  # Output: Whiskers says Meow!
dog.speak()  # Output: Buddy says Woof!