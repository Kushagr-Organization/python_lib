# 4) Find out which student has got highest total marks
student_with_highest_marks = ""
highest_marks = 0

f = open("Total_marks.csv", "r")

for x in f:
    words = x.split(',')
    print(words)
    marks = int(words[1])
    if marks > highest_marks:
        highest_marks = marks
        student_with_highest_marks = words[0]


print(student_with_highest_marks, highest_marks)
