def multiply(a, b):
    return a * b
def add_numbers(a, b):
    return a + b
def subtract_numbers(a, b):
    return a - b
def divide_numbers(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b    
print("====Welcome to the Calculator Program!====")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
print("Select operation:")
print("1. Addition")    
print("2. Subtraction") 
print("3. Multiplication")
print("4. Division")

choice = input("Enter your choice (1/2/3/4): ")

if choice == '1':
    result = add_numbers(num1, num2)
    print(f"The sum of {num1} and {num2} is: {result}") 
elif choice == '2':
    result = subtract_numbers(num1, num2)
    print(f"The difference between {num1} and {num2} is: {result}") 
elif choice == '3':
    result = multiply(num1, num2)
    print(f"The product of {num1} and {num2} is: {result}")
elif choice == '4':
    try:
        result = divide_numbers(num1, num2)
        print(f"The quotient of {num1} and {num2} is: {result}")
    except ValueError as e:
        print(e)            