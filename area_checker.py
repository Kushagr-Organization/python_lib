try:
    l = float(input('Enter length: '))
    b = float(input('Enter breadth: '))
    print('Area =', l * b)
except ValueError:
    print("Please enter valid numbers.")