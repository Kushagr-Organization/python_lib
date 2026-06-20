user_choice = "y"
while user_choice == "y":
    try:
        cp = int(input("What is the cost price?:"))
        sp = int(input("What is the selling price?:"))
        if sp > cp:
            print(f"Profit = Rs {sp - cp}")
        elif cp > sp:
            print(f"Loss = Rs {cp - sp}")
        else:
            print("No profit, no loss")
    except:
        print("Incorrect input given!")

    user_choice = input("Do you want to try again (y/n)?:")

print("Goodbye! Please use again!")
