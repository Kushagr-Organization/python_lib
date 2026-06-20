english = int(input("English marks:"))
hindi = int(input("Hindi marks:"))
science = int(input("Science marks:"))
sst = int(input("SST marks:"))
maths = int(input("Maths marks:")) 
#x = max(science, sst, english, hindi, maths)
max_sub = ""
max_marks = 0

if english > max_marks:
    max_marks = english
    max_sub = "English"

if hindi > max_marks:
    max_marks = hindi
    max_sub = "Hindi"

if science > max_marks:
    max_marks = science
    max_sub = "Science"

if sst > max_marks:
    max_marks = sst
    max_sub  = "SST"

if maths > max_marks:
    max_marks = maths
    max_sub  = "Maths"

print(max_sub, max_marks)
