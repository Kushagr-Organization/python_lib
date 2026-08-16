
print("----------------------------------------------")
print("Welcome to the Trip Mileage Finder!")
print("Let's calculate your trip mileage and fuel cost.")
print("----------------------------------------------")
distance = float(input("Enter the distance of your trip in kilometers: "))
fuel_used = float(input("Enter the amount of fuel used in liters: "))
fuel_price = float(input("Enter the price of fuel per liter: "))
mileage = distance / fuel_used
total_cost = fuel_used * fuel_price
cost_per_km = total_cost / distance
print("\nTrip summary:")
print("----------------------------------------------")
print(f"Distance traveled: {distance} km")
print(f"Fuel used: {fuel_used} liters")
print(f"Mileage: {mileage} km/l")
print(f"Total fuel cost: ₹{total_cost}")
print(f"Average cost per kilometer: ₹{cost_per_km}")
print("----------------------------------------------")
print("Thank you for using the Trip Mileage Finder!")