def my_function(a):
    i = 1
    while i <= 10:
        result = a * i
        print(f"{a} x {i} = {result}")
        i += 1
'''
for x in range(1, 21):
    print(f"Table of {x}")
    my_function(x)
    print("************************************")'''
try:
    user_input = input('what table you want??:')
    y = int(user_input)

    my_function(y)
except:
    print("Wrong input given!")