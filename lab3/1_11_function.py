#11. Write a Python function that checks whether a word or phrase is `palindrome` or not. 
# Note: A palindrome is word, phrase, or sequence that reads the same backward as forward, e.g., madam

def is_palindrome(s):
    s = ''.join(s.split()).lower()
    return s == s[::-1]

text = input("Enter a word or phrase: ")
print("Is palindrome:", is_palindrome(text))
