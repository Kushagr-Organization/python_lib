print("Welcome to the Discount Calculator!")
original_price = float(input("Enter the original price of the item: "))
discount_percentage = float(input("Enter the discount percentage (e.g., 10 for 10%): "))
discount_amount = (discount_percentage / 100) * original_price
final_price = original_price - discount_amount
print("\nOriginal price: ₹", original_price)
print("Discount amount: ₹", discount_amount)
print("Final price after discount", discount_percentage, "%: ₹", final_price)