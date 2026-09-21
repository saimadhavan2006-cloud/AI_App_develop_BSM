from datetime import date
import json

students=[]
def save_data():
    with open("attendance.json","w") as f:
        json.dump(students,f)
def load_data():
    global students
    try:
        with open("attendance.json","r") as f:
            students=json.load(f)
    except FileNotFoundError:
        students=[]
def add_student():
    name=input("Enter student name:")
    student_id=input("Enter student ID:")
    for student in students:
        if student["id"]==student_id:
            print("Student ID already exists.")
            return
    student={"name":name,"id":student_id,"attendance":[]}
    students.append(student)
    save_data()
    print("Student added successfully!")
def view_students():
    if len(students)==0:
        print("No students found.")
    else:
        for student in students:
            print("================")
            print("Name:",student["name"])
            print("ID:",student["id"])
            print("Attendance:",len(student["attendance"]))
def mark_attendance():
    student_id=input("Enter student ID:")
    for student in students:
        if student["id"]==student_id:
            status=input("Enter attendance status (present P/absent A):").upper()
            if status not in ["P","A"]:
                print("Invalid status.")
                return
            student["attendance"].append(status)
            save_data()
            print("Attendance marked successfully!")
            return
    print("Student not found.")
def view_attendance():
    if len(students)==0:
        print("No students found.")
        return
    for student in students:
        attendance=student["attendance"]
        #print("Attendance for",student["name"],"(",student["id"],")")
        print("================")
        print("Name:",student["name"])
        print("ID:",student["id"])
        print("Attendance:",attendance)
        present=attendance.count("P")
        absent=attendance.count("A")
        print("Present:",present)
        print("Absent:",absent)
def attendance_percentage():
    student_id=input("Enter student ID:")
    for student in students:
        if student["id"]==student_id:
            attendance=student["attendance"]
            total=len(attendance)
            present=attendance.count("P")
            if total==0:
                print("No attendance records found.")
                return
            percentage=(present/total)*100
            print("Attendance percentage for",student["name"],"(",student["id"],"):",percentage,"%")
            return
    print("Student not found.")
def search_student():
    student_id=input("Enter student ID:")
    for student in students:
        if student["id"]==student_id:
            print("================")
            print("Name:",student["name"])
            print("ID:",student["id"])
            print("Attendance:",len(student["attendance"]))
            return
    print("Student not found.")
def delete_student():
    student_id=input("Enter student ID:")
    for student in students:
        if student["id"]==student_id:
            students.remove(student)
            save_data()
            print("Student deleted successfully!")
            return
    print("Student not found.")
def main():
    load_data()
    while True:
        print("\nAttendance Tracker Menu:")
        print("1. Add Student")
        print("2. View Students")
        print("3. Mark Attendance")
        print("4. View Attendance")
        print("5. Attendance Percentage")
        print("6. Search Student")
        print("7. Delete Student")
        print("8. Exit")
        choice=input("Enter your choice (1-8):")
        if choice=="1":
            add_student()
        elif choice=="2":
            view_students()
        elif choice=="3":
            mark_attendance()
        elif choice=="4":
            view_attendance()
        elif choice=="5":
            attendance_percentage()
        elif choice=="6":
            search_student()
        elif choice=="7":
            delete_student()
        elif choice=="8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
main()