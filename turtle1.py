from turtle import *

'''screen = turtle.Screen()
t = turtle.Turtle()
print(type(screen))
t.forward(100)
t.right(90)
t.forward(100)
t.right(90)
t.forward(100)
t.right(90)
t.forward(100)
screen.mainloop()  # Keeps the window open'''
'''screen = turtle.Screen()
t = turtle.Turtle()
t.color("red")
t.speed(5)

t.begin_fill()
for i in range(4):
    t.forward(100)
    t.right(90)
t.end_fill()
screen.mainloop()'''
'''import turtle

screen = turtle.Screen()
t = turtle.Turtle()
t.color("red")
t.width(5)
t.speed(10)

for i in range(4):
    t.forward(100)
    t.right(90)

t.begin_fill()

for steps in range(100):
    for c in ('blue', 'red', 'green','yellow'):
        t.color(c)
        t.forward(steps)
        t.right(30)

screen.mainloop()'''
import turtle as t
from random import random
'''
for i in range(1000000000000):
    steps = int(1)
    angle = int(i/100)
    t.right(angle)
    t.fd(steps)'''
bgcolor("light blue")
a = 40
for c in ('orange', 'white', 'green'):

    t.color(c)
    t.width(10)
    t.circle(a)
    t.penup()
    t.right(90)
    t.forward(40)
    t.left(90)
    #t.forward(2*a)
    t.pendown()
    a = a + 40
hideturtle()
t.mainloop()

'''screen = t.Screen
color("black", "red")
begin_fill()
circle(80)
end_fill()'''

'''s = t.Shape("compound")
poly1 = ((0,0),(10,-5),(0,10),(-10,-5))
s.addcomponent(poly1, "red", "blue")
poly2 = ((0,0),(10,-5),(-10,-5))
s.addcomponent(poly2, "blue", "red")'''
hideturtle()
mainloop()