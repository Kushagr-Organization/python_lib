try:
    name = input("What is your name? ")
    age = int(input(f"What is your age, {name} ? "))
    if age >= 18 and age < 60:
        print(f"you are an adult, {name}")
    elif age >= 13 and age < 18:
        print(f"you are a teenager, {name}")
    elif age >= 60:
        print(f"you are a senior citizen, {name}")
    else:
        print(f"you are a child, {name}")
except:
    print("incorrect value for age!")