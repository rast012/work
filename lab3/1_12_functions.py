def histogram(lst):
    for num in lst:
        print('*' * num)

# Example usage:
numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))
histogram(numbers)
