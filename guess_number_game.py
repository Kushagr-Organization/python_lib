import random

secret = (random.randint(1, 100))
attempts = 0

print("🎯 Welcome to Guess the Number!")
print("I'm thinking of a number between 1 and 100.")

while True:
    try:
        guess = int(input("Enter your guess: "))
        attempts += 1
    except ValueError:
        print("Please enter a valid number.")
        continue

    if guess < secret:
        print("📉 Too low!")
    elif guess > secret:
        print("📈 Too high!")
    else:
        print(f"🎉 Correct! You guessed the number in {attempts} attempts.")
        break

play_again = input("Play again? (yes/no): ").lower()

if play_again == "yes":
    print("Restart the program to play again.")
else:
    print("Thanks for playing!")