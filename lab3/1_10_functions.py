#10. Write a Python function that takes a list and returns a new list with unique elements of the first list. 
# Note: don't use collection `set`.

def unique_list(lst):
    unique = []
    for item in lst:
        if item not in unique:
            unique.append(item)
    return unique

numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))
print("Unique elements:", unique_list(numbers))
