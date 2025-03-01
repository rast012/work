# 1. Create a generator that generates the squares of numbers up to some number `N`.
def square_generator(N):
    for i in range(N + 1):
        yield i * i
print()
# 2. Write a program using generator 
# to print the even numbers between 0 and `n` in comma separated form where `n` is input from console.
def even_generator(n):
    for i in range(0, n + 1, 2):
        yield i
n = int(input("Enter a number: "))
print("Even numbers:", end=" ")
for num in even_generator(n):
    print(num, end=",")
print("\b ")


# 3. Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, 
# between a given range 0 and `n`.
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

# 4. Implement a generator called `squares` 
# to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

# Test 
for val in squares(2, 6):
    print(val)

# 5. Implement a generator that returns all numbers from (n) down to 0.
def countdown(n):
    while n >= 0:
        yield n
        n -= 1

# Test 
for num in countdown(5):
    print(num)
