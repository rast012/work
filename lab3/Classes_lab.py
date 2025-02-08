class StringManipulator:
    def __init__(self):
        self.text = ""

    def getString(self):
        self.text = input("Enter a string: ")

    def printString(self):
        print(self.text.upper())

# Example usage:
obj = StringManipulator()
obj.getString()
obj.printString()

class Shape:
    def __init__(self):
        pass

    def area(self):
        return 0

class Square(Shape):
    def __init__(self, length):
        self.length = length

    def area(self):
        return self.length * self.length

# Example usage:
square = Square(4)
print(square.area())  # Output: 16

class Rectangle(Shape):
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

# Example usage:
rectangle = Rectangle(4, 5)
print(rectangle.area())  # Output: 20

import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self):
        print(f"Point coordinates: ({self.x}, {self.y})")

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def dist(self, other_point):
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)

# Example usage:
p1 = Point(1, 2)
p2 = Point(4, 6)

p1.show()
p2.show()

print(p1.dist(p2))  # Output: Distance between p1 and p2

class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        elif amount > 0:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        else:
            print("Withdrawal amount must be positive.")

# Example usage:
acc = Account("John", 100)
acc.deposit(50)
acc.withdraw(30)
acc.withdraw(200)  # Should print "Insufficient funds."

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

numbers = [10, 15, 3, 7, 19, 22, 31, 42, 53]
prime_numbers = list(filter(lambda x: is_prime(x), numbers))

print(prime_numbers)  # Output: [3, 7, 19, 31, 53]
