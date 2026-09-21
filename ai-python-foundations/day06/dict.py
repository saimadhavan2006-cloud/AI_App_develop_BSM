#dictionary
student = {
    "name": "Madhu",
    "age": 20,
    "branch": "ece",
    "cgpa": 7.8
}
print(student["age"])
print(student["name"])
del student["cgpa"]
print(student)

#nested dictionary
students = {
    1:{"name":"madhu","age":20,"branch":"ece"},
    2:{"name":"sonu","age":19,"branch":"cse"},
    3:{"name":"tillu","age":21,"branch":"eee"},
    4:{"name":"tony","age":22,"branch":"civil"},
    5:{"name":"bruce","age":23,"branch":"mech"},
    6:{"name":"swapna","age":21,"branch":"chem"}
}
print(students[5]["name"])