### Read in a Fahrenheit temperature. Calculate and display the equivalent centigrade temperature. 
# The following formula is used for the conversion:`C = (5 / 9) * (F – 32)`
temp = int(input("Enter the temperature in Farenheits: "))
def myfunc(F):
    return((F-32)*5/9)
print(myfunc(temp))