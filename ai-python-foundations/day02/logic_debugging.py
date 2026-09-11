#finding the second largest number in a list of numbers
l1 = list(input("Enter the list of numbers separated by spaces: ").split())
first_largest_no = 0
second_largest_no = 0
for i in l1:
    if int(i) > first_largest_no:
        second_largest_no = first_largest_no
        first_largest_no = int(i)
    elif int(i) > second_largest_no:
        second_largest_no = int(i)
print("The second largest number is:", second_largest_no)

#mutable and immutable data types
a = [10, 20, 30]
c = a.copy()
b = a
b.append(40)
print(c)
print(b)

#debugging the code
'''numbers = [10, 20, 30, 40, 50]
total = 0
for i in range(1, len(numbers)):
 total = total + numbers[i]
print("Total:", total)
Expected output: Total: 150'''
#here, i is starting from 1, so it is skipping the first element of the list. To fix this, we should start the range from 0 instead of 1.
numbers = [10, 20, 30, 40, 50]
total = 0
for i in range(0, len(numbers)):
 total += numbers[i]
print("Total:", total)
#Expected output: Total: 150