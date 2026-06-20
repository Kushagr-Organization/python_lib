f = open("Marks_File.csv", "r")
student_name = (input("student name: "))
print(student_name)
student_found_switch = 'no'

sum = 0 
for x in f:
   # print("loop has started")
    #print(x)
    words = x.split(',')
    if student_name in words[0]:
        student_found_switch = "yes"
        marks = int(words[2])
        sum = sum + marks
      #  print(words[2])
   # print("loop has ended")

if student_found_switch == "yes":
    print("total marks = ", sum)
    print(f"{student_name} has got {sum / 240 * 100 }% as the total percentage!")
else:
    print("This student's name is not the list!")


    
'''
f = open("demofile.txt", "a")
f.write("Now the file has more content!")
f.close()'''


# 1) Take the input student name and show all his/her subject marks
# 2) Show the total marks of input student name
# 3) Show the total percentage of input student name
# 4) Find out which student has got highest total marks

