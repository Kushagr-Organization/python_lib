def area_rectangle(l, b):
    area = l * b
    return area

user_choice = "y"

while user_choice == "y":
    try:
        length = int(input("length is :"))
        breadth = int(input("breadth is :"))
        x = area_rectangle(length,breadth)
        print(f"The length is {length}. The breadth is {breadth}. The area is {x}")
    except:
        print("Incorrect input was given!")
    
    user_choice = input("Do you want to try again (y/n)?:")

