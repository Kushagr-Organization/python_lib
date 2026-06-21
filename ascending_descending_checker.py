num_1 = 0
num_2 = 0
num_3 = 0
num_4 = 0
num_5 = 0

numbers = []
for i in range(5):
    value = float(input(f"Enter number {i + 1}: "))
    numbers.append(value)

order = input("Type 'ascending' or 'descending': ").strip().lower()

if order == "ascending":
    numbers.sort()
elif order == "descending":
    numbers.sort(reverse=True)
else:
    print("Invalid choice, using ascending by default.")
    numbers.sort()

print("Sorted numbers:", numbers)