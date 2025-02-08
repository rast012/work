#9. Write a function that computes the volume of a sphere given its radius.
def sphere_volume(radius):
    return (float(4/3) * 3.14 * (radius ** 3))

# Example usage:
radius = float(input("Enter the radius of the sphere: "))
print("Volume of the sphere:", sphere_volume(radius))
