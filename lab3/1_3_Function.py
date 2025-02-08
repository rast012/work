###Write a program to solve a classic puzzle: 
#We count 35 heads and 94 legs among the chickens and rabbits in a farm. How many rabbits and 
#how many chickens do we have? `create function: solve(numheads, numlegs):`

a, b = int(input("Enther the number of heads and number of legs: "))
def myfunc(head, legs):
    rabbit = legs-2 * head
    chicken = head - rabbit
    print("Number of rabbits: " + rabbit)
    print("Number of chickens: " + chicken)
