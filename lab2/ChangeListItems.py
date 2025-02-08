thislist = ["1", "2", "3"]
thislist[1] = "0"
print(thislist) 
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]
thislist[1:3] = ["blackcurrant", "watermelon"]
print(thislist) #replacing in a period
thislist = ["apple", "banana", "cherry"]
thislist[1:2] = ["blackcurrant", "watermelon"]
print(thislist) #new values will be inserted if more than necessary numbers of values are passed
thislist = ["apple", "banana", "cherry"]
thislist[1:3] = ["watermelon"]
print(thislist) #replacing several items with one 
