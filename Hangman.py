import random
# List of words to choose from

sport =[
    "Soccer", "Basketball", "Baseball", "Cricket", "Tennis", "Table Tennis",
    "Badminton", "Volleyball", "Hockey", "Rugby", "American Football",
    "Golf", "Boxing", "Wrestling", "Martial Arts", "Karate", "Judo",
    "Taekwondo", "Skateboarding", "Surfing", "Skiing", "Snowboarding",
    "Ice Skating", "Swimming", "Cycling", "Running", "Athletics", "Gymnastics",
    "Archery", "Fencing", "Shooting", "Weightlifting", "Rowing", "Canoeing",
    "Sailing", "Climbing", "Horse Riding", "Motorsport", "Esports", "Squash",
    "Kabaddi", "Lacrosse", "Handball", "Polo", "Snooker", "Darts", "Bowling"
]
fruit = [
    "Apple", "Apricot", "Avocado", "Banana", "Blackberry", "Blackcurrant",
    "Blueberry", "Boysenberry", "Breadfruit", "Cantaloupe", "Cherimoya",
    "Cherry", "Chico", "Clementine", "Cloudberry", "Coconut", "Crabapple",
    "Cranberry", "Currant", "Custard Apple", "Date", "Dragonfruit", "Durian",
    "Elderberry", "Feijoa", "Fig", "Goji Berry", "Gooseberry", "Grape",
    "Grapefruit", "Guava", "Hackberry", "Honeyberry", "Honeydew", "Huckleberry",
    "Imbu", "Indian Fig", "Jackfruit", "Jambul", "Jujube", "Juniper Berry",
    "Kaffir Lime", "Kiwano", "Kiwi", "Kumquat", "Langsat", "Lemon", "Lime",
    "Longan", "Loquat", "Lychee", "Mandarin", "Mango", "Mangosteen", "Marionberry",
    "Melon", "Miracle Fruit", "Mulberry", "Nance", "Nectarine", "Olive", "Orange",
    "Papaya", "Passionfruit", "Peach", "Pear", "Persimmon", "Pineapple", "Pitaya",
    "Plantain", "Plum", "Pluot", "Pomegranate", "Pomelo", "Prickly Pear",
    "Quince", "Raisin", "Rambutan", "Raspberry", "Redcurrant", "Rose Apple",
    "Salak", "Sapodilla", "Sapote", "Satsuma", "Soursop", "Star Apple",
    "Starfruit", "Strawberry", "Surinam Cherry", "Tamarillo", "Tamarind",
    "Tangerine", "Ugli Fruit", "Watermelon", "White Currant", "Yuzu"
]
print("🎮 Welcome to Hangman!")
category = input("There are two categories, 1 is for sport and 2 is for fruits. Please select in 1 or 2.")
if category == 1:
    category = fruit

if category == 2:
    category = sport
          
word = random.choice(category).lower() # Randomly pick a word

# Variables to keep track of the game
guessed_letters = []
tries = 10
display = ["_"] * len(word)


print("Guess the word, one letter at a time.")

# Game loop
while tries > 0 and "_" in display:
    print("\nWord:", " ".join(display))
    print("Guessed letters:", guessed_letters)
    print(f"Tries left: {tries}")

    guess = input("Guess a letter: ").lower()

    if not guess.isalpha() or len(guess) != 1:
        print("Please enter a single letter.")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter.")
        continue

    guessed_letters.append(guess)

    if guess in word:
        print("✅ Good guess!")
        for i in range(len(word)):
            if word[i] == guess:
                display[i] = guess
    else:
        print("❌ Wrong guess.")
        tries -= 1

# Game result
if "_" not in display:
    print("\n🎉 Congratulations! You guessed the word:", word)
else:
    print("\n😢 You're out of tries. The word was:", word)     