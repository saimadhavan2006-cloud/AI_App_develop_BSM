import math

print("----calculator----")
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
print("\n----operations----")
print("1.addition","\n2.subtraction","\n3.multiplication","\n4.division","\n5.modulus","\n6.exponentiation","\n7.floor division","\n8.sine of first number","\n9.cosine of first number","\n10.tangent of first number","\n11.logarithm of second number","\n12.square root of sum of two numbers")
choice = int(input("Enter your choice(1-12): "))
#looping through the operations based on user choice
if choice == 1:
    print("Addition:", a + b)
elif choice == 2:
    print("Subtraction:", a - b)
elif choice == 3:
    print("Multiplication:", a * b)
elif choice == 4:
    print("Division:", a / b)
elif choice == 5:
    print("Modulus:", a % b)
elif choice == 6:
    print("Exponentiation:", a ** b)      #if and elif are control flow statements that allow you to execute different blocks of code based on certain conditions. 
elif choice == 7:                         #In this case, the program checks the user's choice and performs the corresponding mathematical operation.
    print("Floor Division:", a // b)
elif choice == 8:
    print("Sine of first number :", math.sin(a))
elif choice == 9:
    print("Cosine of first number :", math.cos(a))
elif choice == 10:
    print("Tangent of first number :", math.tan(a))
elif choice == 11:
    print("Logarithm of second number :", math.log(b))
elif choice == 12:
    print("Square root of sum of two numbers :", math.sqrt(a + b))
else:
    print("Invalid choice!")