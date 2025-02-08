thislist = ["apple", "banana", "cherry"]
thislist.remove("banana")
print(thislist)

thislist = ["apple", "banana", "cherry", "banana", "kiwi"]
thislist.remove("banana")
print(thislist) #["apple", "cherry", "banana", "kiwi"]

thislist = ["apple", "banana", "cherry"]
thislist.pop(1)
print(thislist) #["apple", "cherry"]

thislist = ["apple", "banana", "cherry"]
thislist.pop()
print(thislist) #["apple", "banana"]

thislist = ["apple", "banana", "cherry"]
del thislist[0]
print(thislist) #["banana", "cherry"]

thislist.clear()
print(thislist) #[]

thislist = ["apple", "banana", "cherry"]
del thislist 
#print(thislist) won't work, since we delete the entire list, not only its contents
