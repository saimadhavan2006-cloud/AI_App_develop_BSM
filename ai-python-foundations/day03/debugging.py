#debugging challenge
def calculate_total(price, quantity):
    total = price * quantity
    print(total)
    return total  #returning the total value so that it can be used outside the function

result = calculate_total(100, 3)
discount = result * 0.10
print("Discount:", discount)

"""def calculate_total(price, quantity):
 total = price * quantity
 print(total)
result = calculate_total(100, 3)
discount = result * 0.10
print("Discount:", discount)"""