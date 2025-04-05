#1. Write a Python program to list only directories, files and all directories, files in a specified path. 
import math
a = [2, 4, 8, 3]
res = math.prod(a)  
print(res)

#2. Write a Python program with builtin function that accepts a string and calculate 
# the number of upper case letters and lower case letters
s = str(input())
sum = 0
for i in s:
    if i.isupper():
        sum+=1
print(sum)

#3. Write a Python program with builtin function that checks whether a passed string is palindrome or not.
def my_function(x):
  return x[::-1]
if s != my_function(s):
   print("Not Palindrome")
else:
   print("Palindrome")

#4 Write a Python program that invoke square root function after specific milliseconds. 
#Sample Input:
#25100
#2123
#Sample Output:
#Square root of 25100 after 2123 miliseconds is 158.42979517754858

import time
s = int(input())
ms = int(input())
time.sleep(ms/1000)
print("Square root of " + str(s) + " after " + str(ms) + " miliseconds is " + str(s**1/2))

#5. Write a Python program with builtin function that returns True if all elements of the tuple are true.
def check_true(t1):
    for t in t1:
        if not bool(t):
            return False
    return True
t = (True, 1, "hello")  
print(check_true(t))  
t = (True, 0, "hello")  
print(check_true(t))  
