pair = [10,15]
x, y = pair # unpacking
print(x,y)

a = pair[0] # selection operator

from operator import getitem
b = getitem(pair, 0) # selection function

print(a,b)