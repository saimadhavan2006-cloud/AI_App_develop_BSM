import json
student = {
  "name": "Anil",
  "age": 22,
  "branch": "CSE"
}
json_string=json.dumps(student)
print(json_string)
with open("student.json","w") as f:
    json.dump(student,f)
