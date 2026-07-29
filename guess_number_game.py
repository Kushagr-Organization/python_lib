import random

print("🎯 Welcome to Guess the Number!")
print("I'm thinking of a number between 1 and 100.")

play_again = "yes"

while play_again.lower() != "no":
    secret = random.randint(1, 100)
    attempts = 0

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
            play_again = input("Play again? (yes/no): ").strip().lower()
            break

    if play_again == "no":
        print("Thanks for playing!")