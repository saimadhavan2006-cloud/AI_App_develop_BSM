students = ["Maddy", "Dileep", "Harsha", "Dhanush", "Sanjay"]
age = [20, 21, 22, 23, 24]
mixed = ["hello", 1, 2.5, True, None]
print(mixed[3])
mixed[3] = "Raju"
print(mixed[3])
mixed.append("Symala")
print(mixed)
mixed.insert(2,"radha")
print(mixed)
mixed.remove(1)
print(mixed)
mixed.pop(2)
print(mixed)
mixed.pop()
print(mixed)
print(len(mixed))
for i in range(len(mixed)):
    print(mixed[i])