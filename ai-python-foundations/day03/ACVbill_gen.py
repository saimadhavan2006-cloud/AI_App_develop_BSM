print("=====Amma Chethi Vanta(A.C.V) Bill Generator=====")

#giving the details of the bill

n = int(input("Enter the number of items: "))
subtotal = 0
for i in range(n):
    print("\n Enter the details for item", i + 1)
    item_name = input("Enter the name of the item: ")
    item_price = float(input("Enter the price of the item: "))
    quantity = int(input("Enter the quantity of the item: "))
    item_total = item_price * quantity
    subtotal += item_total

#entering the tax rate and calculating the final amount

tax_rate = float(input("Enter the tax rate (in percentage): "))
tax_amount = (subtotal * tax_rate) / 100
final_amount = subtotal + tax_amount

#entering the service charge rate and calculating the final amount with service charge

service_charge_rate = float(input("Enter the service charge rate (in percentage): "))
service_charge_amount = (subtotal * service_charge_rate) / 100  
final_amount += service_charge_amount

#initially displaying the bill summary with service charge included

print("\n=====Bill Summary=====")
print("Subtotal: $", round(subtotal, 2), 
      "\nTax Amount: $", round(tax_amount, 2), 
      "\nFinal Amount: $", round(final_amount, 2))

#asking the user if they want to remove the service charge and updating the final amount accordingly

remove_service_charge = input("\nDo you want to remove the service charge? (yes/no): ")
if remove_service_charge.lower() == "yes":
    final_amount -= service_charge_amount
    print("\nService charge removed.")
    print("Final Amount after removing service charge: $", round(final_amount, 2))  
else:
    print("\n=====final Bill Summary=====")
    print("\nService charge retained.")
    print("Final Amount with service charge: $", round(final_amount, 2))    