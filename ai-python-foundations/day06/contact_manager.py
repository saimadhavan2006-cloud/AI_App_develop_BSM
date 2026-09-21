'''add
view
search
update
delete
exit'''
# 1. Initialize the contacts list
contacts = []

import re

def is_valid_phone(phone):
    """
    Validates a phone number. 
    Matches exactly 10 digits (e.g., 9876543210).
    """
    pattern = r"^\d{10}$"
    return bool(re.match(pattern, phone))

def is_valid_gmail(email):
    """
    Validates a Gmail address.
    Ensures it starts with valid characters and ends strictly with @gmail.com.
    """
    pattern = r"^[a-zA-Z0-9._]+@gmail\.com$"
    return bool(re.match(pattern, email))    

def add_contact():
    name = input("Enter name: ")
    
    # Keep asking until a valid 10-digit phone number is entered
    while True:
        phone = input("Enter phone (10 digits): ")
        if is_valid_phone(phone):
            break
        print("Invalid phone format. Please enter exactly 10 digits.")
        
    # Keep asking until a valid Gmail address is entered
    while True:
        email = input("Enter Gmail address: ")
        if is_valid_gmail(email):
            break
        print("Invalid email format. Please enter a valid @gmail.com address.")
        
    contact = {"name": name, "phone": phone, "email": email}
    contacts.append(contact)
    print("Contact added successfully!")



def view_contacts():
    # 3. Corrected variable name from 'contact' to 'contacts'
    if len(contacts) == 0:
        print("No contacts found.")
    else:
        for contact in contacts:
            print("=============")
            print("Name:", contact["name"])
            print("Phone:", contact["phone"])
            print("Email:", contact["email"])
            print("=============")  

def search_contact():
    l1 = input("Enter name to search: ")
    for contact in contacts:
        if contact["name"].lower() == l1.lower():
            print("==============")
            print("Name:", contact["name"])
            print("Phone:", contact["phone"])
            print("Email:", contact["email"])
            return 
    print("Contact not found.")

def update_contact():
    name = input("Enter name to update: ")
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            phone = input("Enter new phone: ")
            email = input("Enter new email: ")
            contact["phone"] = phone
            contact["email"] = email
            print("Contact updated successfully")
            return
    print("Contact not found")

def delete_contact():
    name = input("Enter name to delete: ")
    for contact in contacts:
        if contact["name"].lower() == name.lower():
            contacts.remove(contact)
            print("Deleted successfully")
            return
    print("Contact not found")

while True:
    print("\n1. Add contact \n2. View contact \n3. Search contact \n4. Update contact \n5. Delete contact \n6. Exit")
    
    # Added basic error handling to prevent crashes on invalid input
    try:
        choice = int(input("Enter the choice(1-6): "))
    except ValueError:
        print("Invalid input, please enter a number.")
        continue

    if choice == 1:
        add_contact()
    elif choice == 2:
        view_contacts()
    elif choice == 3:
        search_contact()
    elif choice == 4:
        update_contact()
    elif choice == 5:
        delete_contact() 
    elif choice == 6:
        print("Exiting program...")
        break
    else:
        print("Invalid choice, please try again")                   