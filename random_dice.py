import random
choice = "y"
kush_counter = 0
alka_counter = 0
nitesh_counter = 0
python_counter = 0
loop_counter = 0

while  loop_counter < 10:
    kush = int(input("Kushagr - Enter your Guess: "))
    alka = int(input("Alka - Enter your Guess: "))
    nitesh = int(input("Nitesh - Enter your Guess: "))

    x = random.randint(1,6)
    print(x)
    if kush == x:
        print("You are Lucky, Kushagr")
        kush_counter = kush_counter + 1
    elif alka == x:
        print("Alka is right")
        alka_counter = alka_counter + 1
    elif nitesh == x:
        print("Nitesh is always Right")
        nitesh_counter = nitesh_counter + 1
    else:
        print("Hard Luck Everyone, Python is smarter than all of you,  Try Again")
        python_counter = python_counter + 1
    loop_counter = loop_counter + 1
    #choice = input("Do you want to try again: ")
print(" Kushagr's score is " , kush_counter)
print("Alka's score is ", alka_counter)
print("Nitesh's score is ", nitesh_counter)
print("Python's score is ", python_counter)

