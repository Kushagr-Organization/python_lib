'''
def print_name():
    name = "Nitesh"
    print(name)

def print_student_name():
    name = "Alka"
    print(name)

try:
    print_name()
    name = "Kushagr"

    print_student_name()
    print(name)
except:
    print("Error::::Variable not defined")
    '''

a = 1

# Uses global because there is no local 'a'
def f():
    print('Inside f() : ', a)

# Variable 'a' is redefined as a local
def g():
    a = 2
    print('Inside g() : ', a)

# Uses global keyword to modify global 'a'
def h():
    global a
    a = 3
    print('Inside h() : ', a)


# Global scope
print('global : ', a)
f()
print('global : ', a)
g()
print('global : ', a)
h()
print('global : ', a)
