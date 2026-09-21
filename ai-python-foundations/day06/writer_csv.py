from csv import writer
import csv
with open("user.csv","w",newline="") as f:
    writer=csv.writer(f)
    writer.writerow(["Name","Age","Marks"])
    writer.writerow(["Madhu",20,87])