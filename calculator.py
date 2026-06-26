try:
    num_1 = float(input("Enter the first number: "))
    num_2 = float(input("Enter the second number: "))
except ValueError:
    print("Error: Invalid input. Please enter numeric values.")
    exit()
operation = input("Enter the operation (+, -, *, /): ")

if operation == '+':
    result = num_1 + num_2
    print(f"The result of {num_1} + {num_2} is: {result}")
elif operation == '-':
    result = num_1 - num_2
    print(f"The result of {num_1} - {num_2} is: {result}")
elif operation == '*':
    result = num_1 * num_2
    print(f"The result of {num_1} * {num_2} is: {result}")
elif operation == '/':
    if num_2 != 0:
        result = num_1 / num_2
        print(f"The result of {num_1} / {num_2} is: {result}")
    else:
        print("Error: Division by zero is not allowed.")
else:
    print("Error: Invalid operation.")