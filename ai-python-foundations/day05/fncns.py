def add_numbers(a, b):
    """
    Add two numbers together.

    Parameters:
    a (float): The first number.
    b (float): The second number.

    Returns:
    float: The sum of the two numbers.
    """
    return a + b
n1 = float(input("Enter the first number: "))
n2 = float(input("Enter the second number: "))      
print(f"The sum of {n1} and {n2} is: {add_numbers(n1, n2)}")
#return statement is used to return the value from the function 
#print statement is used to print the sum of two numbers.