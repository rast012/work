import re

# 1. Match 'a' followed by zero or more 'b's
def match_a_b(string):
    return bool(re.fullmatch(r'a*b*', string))

print(match_a_b("ab"))  # True
print(match_a_b("a"))   # True
print(match_a_b("abb")) # True
print(match_a_b("b"))   # False

# 2. Match 'a' followed by two to three 'b's
def match_a_bb(string):
    return bool(re.fullmatch(r'ab{2,3}', string))

print(match_a_bb("abb"))   # True
print(match_a_bb("abbb"))  # True
print(match_a_bb("ab"))    # False

# 3. Find sequences of lowercase letters joined with an underscore
def find_lowercase_underscore(string):
    return re.findall(r'\b[a-z]+_[a-z]+\b', string)

print(find_lowercase_underscore("hello_world test_example abc_def_ghi")) 

# 4. Find sequences of one uppercase letter followed by lowercase letters
def find_upper_lower(string):
    return re.findall(r'\b[A-Z][a-z]+\b', string)

print(find_upper_lower("Hello World This Is Test"))

# 5. Match 'a' followed by anything, ending in 'b'
def match_a_anything_b(string):
    return bool(re.fullmatch(r'a.*b', string))

print(match_a_anything_b("acb"))  # True
print(match_a_anything_b("a123b"))  # True
print(match_a_anything_b("ab"))  # True
print(match_a_anything_b("abc"))  # False

# 6. Replace spaces, commas, or dots with colons
def replace_with_colon(string):
    return re.sub(r'[ ,.]', ':', string)

print(replace_with_colon("Hello, world. This is a test"))

# 7. Convert snake_case to camelCase
def snake_to_camel(string):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), string)

print(snake_to_camel("hello_world_test"))  # helloWorldTest

# 8. Split a string at uppercase letters
def split_at_uppercase(string):
    return re.split(r'(?=[A-Z])', string)

print(split_at_uppercase("SplitAtUppercaseLetters"))

# 9. Insert spaces between words starting with capital letters
def insert_spaces(string):
    return re.sub(r'(?<!^)(?=[A-Z])', ' ', string)

print(insert_spaces("ThisIsATestString"))  # This Is A Test String

# 10. Convert camelCase to snake_case
def camel_to_snake(string):
    return re.sub(r'([A-Z])', r'_\1', string).lower().lstrip('_')

print(camel_to_snake("camelCaseString"))  # camel_case_string
