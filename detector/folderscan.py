# import OS
import os
 
# input variable for implementation
dir = input(r"Enter the path of the folder: ")
con = []

con.append(dir)
# start; goes to path
for x in os.listdir(dir):
    # searches for specific filetypes
    if x.endswith(".py"):
        con.append(x)
    
# eliminates empty strings from list
con = list(filter(None, con))
print(con)

# prints each element of list
n = 0
while n < len(con):
    print(con[n])
    n += 1