x = "awesome"
def myfunc():
  print("Python is " + x)
myfunc()


#the local function takes priority when it is announced inside the function
def myfunc1():
  x = "A"
  print("Python is " + x)
myfunc1()
#the output is Python is A