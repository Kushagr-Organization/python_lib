import random

def ask_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-'])

    if operator == '+':
        correct_answer = num1 + num2
    else:
        correct_answer = num1 - num2

    print(f"What is {num1} {operator} {num2}?")
    try:
        user_answer = int(input("Your answer: "))
        if user_answer == correct_answer:
            print("✅ Correct!\n")
            return True
        else:
            print(f"❌ Wrong. The correct answer was {correct_answer}.\n")
            return False
    except ValueError:
        print("❗ Please enter a number.\n")
        return False

def run_quiz():
    print("🧠 Welcome to the Math Quiz!")
    score = 0
    total_questions = 5

    for i in range(total_questions):
        print(f"\nQuestion {i + 1} of {total_questions}")
        if ask_question():
            score += 1

    print(f"\n🎉 Quiz Over! You scored {score} out of {total_questions}.")

if __name__ == "__main__":
    run_quiz()
