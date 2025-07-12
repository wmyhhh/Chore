from datetime import date

# date is a class
# print(type(date))

today = date(2025, 7, 11)
end_of_freedom = date(2025, 9, 15)

length = str(end_of_freedom - today)
print(length)

# attributes
y = today.year
m = today.month

# methodes: attributes bond to functions
x = today.strftime('%A %B %d')
print(x) # return: Friday July 11

'''object 
consist of data and behaviors
a type of object is called class
in python every value is an object
'''