from turtle import *
# SCREEN SETUP
speed(1)
setup(800, 500)

penup()
goto(-400, 250)
pendown()

#THE ORANGE PART
color("orange")
begin_fill()
forward(800)
right(90)
forward(167)
right(90)
forward(800)
end_fill()
penup()
left(90)
forward(167)
pendown()

# THE GREEN PART
color("green")
begin_fill()
forward(167)
left(90)
forward(800)
left(90)
forward(167)
end_fill()

# THE BLUE CIRCLE
penup()
goto(70, 0)
pendown()
color("navy")
begin_fill()
circle(70)
end_fill()

#THE WHITE CIRCLE
penup()
goto(60, 0)
pendown()
color("white")
begin_fill()
circle(60)
end_fill()

#TINY BLUE CIRCLES
penup()
goto(-57, -8)
pendown()
color("navy")
for x in range(24):
    begin_fill()
    circle(3)
    end_fill()
    penup()
    forward(15)
    right(15)
    pendown()

#SMALL BLUE CIRCLE
'''penup()
goto(20, 0)
pendown()
begin_fill()
circle(20)
end_fill()'''

#SPOKES
penup()
goto(0, 0)
pendown()
pensize(4)
for i in range(24):
    forward(60)
    back(60)
    right(15)

hideturtle()
mainloop()