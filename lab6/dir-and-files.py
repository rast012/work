#1 Write a Python program to list only directories, files and all directories, files in a specified path. 
import os
def list_contents(path):
    only_dirs = []
    only_files = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            only_dirs.append(item)
        elif os.path.isfile(item_path):
            only_files.append(item)
    print("Directories:")
    for d in only_dirs:
        print(d)
    print("\nFiles:")
    for f in only_files:
        print(f)
    print("\nAll contents:")
    for i in os.listdir(path):
        print(i)
path = input()
list_contents(path)

#2. Write a Python program to check for access to a specified path. 
#Test the existence, readability, writability and executability of the specified path

def check_path_access(path):
    access_info = {
        "exists?": os.path.exists(path),
        "readable?": os.access(path, os.R_OK),
        "writable?": os.access(path, os.W_OK),
        "executable?": os.access(path, os.X_OK)}
    return {"exists?": False, "readable?": False, "writable?": False, "executable?":False}
path = "/home/rustem"
details = check_path_access(path)
print(details)

#3. Write a Python program to 
# test whether a given path exists or not. If the path exist find the filename and directory portion of the given path. 

def check_path_details(path):
    if os.path.exists(path):
        return {
            "exists": True,
            "directory": os.path.dirname(path),
            "filename": os.path.basename(path)
        }
    return {"exists": False, "directory": None, "filename": None}

path = "/home/rustem"
details = check_path_details(path)
print(details)

#4 Write a Python program to count the number of lines in a text file.
def count_lines_in_file(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            return len(file.readlines())
    return "No such file exists"
file_path = "/home/rustem/test.txt" #jsyk only test.txt exists. 
print(count_lines_in_file(file_path))

#5 Write a Python program to write a list to a file.
def write_list(file_path, list):
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            for i in len(list):
                file.write(list[i])
                file.write("\n") 
list = ["aaa", "\n", 12]

#6. Write a Python program to generate 26 text files named A.txt, B.txt, and so on up to Z.txt
def create_abc():
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in alphabet:
        with open(f"{i}.txt", "x"):
            continue
    print("done")
    return None
create_abc()

#7. Write a Python program to copy the contents of a file to another file  
def copy_AtoB(A, B):
    source = open(A, 'r')  
    destination = open(B, 'w')  
    for line in source:
        destination.write(line)
    source.close()  
    destination.close()  
copy_AtoB("test.txt", "te.txt")

#8. Write a Python program to delete file by specified path. 
# Before deleting check for access and whether a given path exists or not.

def delete_file(file_path):
    if os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.W_OK):
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    else:
        print(f"File '{file_path}' does not exist or cannot be deleted.")

file_path = "/home/rustem/Projects/g.txt"
delete_file(file_path)