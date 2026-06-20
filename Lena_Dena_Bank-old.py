print("Welcome to Lena Dena Bank")
account = str(input("Do you want to create a bank account?: "))
if account == "yes" or account == "Yes":
    name_1 = input("Enter your name: ")
    age_1 = input("Enter your age: ")

elif account == "no" or account == "No":
    print("Thanks for visiting our app. Please spread our name to everyone you know.")

else:
    print("Please give your answer in yes or no")
    account = str(input("Do you want to create a bank account?: "))

    if account == "yes" or account == "Yes":
        name_1 = input("Enter your name: ")
        age_1 = input("Enter your age: ")

    elif account == "no" or account == "No":
        print("Thanks for visiting our app. Please spread our name to everyone you know.")

    else:
        print("Please give your answer in yes or no")
        account = str(input("Do you want to create a bank account?: "))

        if account == "yes" or account == "Yes":
            name_1 = input("Enter your name: ")
            age_1 = input("Enter your age: ")

        elif account == "no" or account == "No":
            print("Thanks for visiting our app. Please spread our name to everyone you know.")

        else:
            print("Since you did not answer in yes or no, YOU ARE BLACKLISTED")