import turtle
import random
import time

# Set up the screen
print("check the turtle screen in a separate window")
print("added additional print line")
screen = turtle.Screen()
screen.title("Turtle Race Game")
screen.bgcolor("lightblue")

# Create a finish line
finish_line = 200
line = turtle.Turtle()
line.penup()
line.goto(finish_line, 150)
line.right(90)
line.pendown()
line.forward(300)
line.hideturtle()

# Create player 1 turtle
turtle1 = turtle.Turtle()
turtle1.color("green")
turtle1.shape("turtle")
turtle1.penup()
turtle1.goto(-200, 50)
turtle1.pendown()

# Create player 2 turtle
turtle2 = turtle.Turtle()
turtle2.color("orange")
turtle2.shape("turtle")
turtle2.penup()
turtle2.goto(-200, -50)
turtle2.pendown()

# Countdown before race starts
countdown = turtle.Turtle()
countdown.hideturtle()
countdown.penup()
countdown.goto(0, 200)
for i in range(3, 0, -1):
    countdown.write(f"Starting in {i}", align="center", font=("Arial", 24, "bold"))
    time.sleep(1)
    countdown.clear()
countdown.write("Go!", align="center", font=("Arial", 24, "bold"))
time.sleep(1)
countdown.clear()

# Start race
winner = None
while True:
    turtle1.forward(random.randint(1, 10))
    turtle2.forward(random.randint(1, 10))
   
    if turtle1.xcor() >= finish_line:
        winner = "Green Turtle"
        break
    if turtle2.xcor() >= finish_line:
        winner = "Orange Turtle"
        break

# Show winner
result = turtle.Turtle()
result.hideturtle()
result.penup()
result.goto(0, 0)
result.write(f"{winner} wins!", align="center", font=("Arial", 30, "bold"))

# Keep the window open until closed manually
screen.mainloop()
