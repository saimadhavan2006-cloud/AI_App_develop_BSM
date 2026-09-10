#list
l1 = [1, 2, 3, 4.52, 5,"maddy"]
print(l1[5]) #maddy
l1[4] = "bhuvi"
print(l1) 
#tuple
tup1 = (1, 2, 3, 4.52, 5,"maddy")
print(tup1[2]) 
l2 = list(tup1)
print(l2)
tup2 = tuple(l1)
print(tup2)
#dictionary
dict1 = {"name":"maddy", "age": 20, "city": "hyderabad"}
print(dict1["name"])

