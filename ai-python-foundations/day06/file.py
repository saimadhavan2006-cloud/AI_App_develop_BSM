'''name = input("enter the name:")
with open("user.txt","w") as f:
    f.write(name)'''
'''with open("user.txt","r") as f:
    print(f.read())'''
with open("user.txt", "a") as f:
    f.write("\n")
    f.write("bsbk")