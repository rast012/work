import math

# 1. Convert degree to radian
def degree_to_radian(degree):
    return round(degree * (math.pi / 180), 6)
degree = float(input("degree: "))
print(degree_to_radian(degree))

# 2. Calculate the area of a trapezoid
def trapezoid_area(height, base1, base2):
    return (1/2) * (base1 + base2) * height
height = float(input("Height: "))
base1 = float(input("Base 1: "))
base2 = float(input("base 2: "))
print(trapezoid_area(height, base1, base2))

# 3. Calculate the area of a regular polygon
def regular_polygon_area(n_sides, side_length):
    return round((n_sides * (side_length ** 2)) / (4 * math.tan(math.pi / n_sides)), 2)
n_sides = int(input("number of sides: "))
side_length = float(input("length of a side:"))
print(regular_polygon_area(n_sides, side_length))

# 4. Calculate the area of a parallelogram
def parallelogram_area(base, height):
    return base * height
base = float(input("Length: "))
height = float(input("Height: "))
print(parallelogram_area(base, height))
