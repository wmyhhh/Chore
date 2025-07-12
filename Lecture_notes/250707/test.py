a = sum([[1], [2]], [])
b = sum([[1, [2], [[3]]]], [4, 5])
print(a)
print(b)
'''
how GPT explains
✅ sum() function (with sequences)

Syntax:
sum(iterable, start)

iterable: Something like a list, tuple, etc., that you can iterate over.

start: The initial value. For numbers it's often 0. But when summing lists, the start must be a list (usually an empty list []).

When used on lists, sum() will concatenate all the lists together.

'''

l = [1, 2, 3]
print(sum(l), list(l))

p = [1, 2, [3, [4]]]
print(list(p))

q = []
print(list(q))